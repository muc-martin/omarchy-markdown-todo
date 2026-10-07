pragma ComponentBehavior: Bound
import QtQuick
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui

Panel {
  id: root
  moduleName: "martin.todo"
  ipcTarget: "martin.todo"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  property var sections: ({ P0: [], P1: [], P2: [] })
  property var expanded: ({ P0: true, P1: false, P2: false })
  property bool defaultExpansionPending: false
  property string errorText: ""
  property string actionError: ""
  readonly property color ink: bar ? bar.foreground : Color.foreground
  readonly property color hoverTint: Qt.rgba(ink.r, ink.g, ink.b, 0.09)
  readonly property var priorities: ["P0", "P1", "P2"]

  function itemsFor(priority) {
    return sections && sections[priority] ? sections[priority] : []
  }

  function openItemsFor(priority) {
    return itemsFor(priority).filter(function(task) { return !task.done })
  }

  function openCount(priority) {
    var items = itemsFor(priority)
    var count = 0
    for (var i = 0; i < items.length; i++) if (!items[i].done) count++
    return count
  }

  function refresh() {
    if (!loadProcess.running) loadProcess.running = true
  }

  readonly property string helperPath: decodeURIComponent(Qt.resolvedUrl("omarchy-todo").toString().replace(/^file:\/\//, ""))

  function helperCommand(args) {
    var command = ["python3", helperPath]
    var file = String(setting("file", ""))
    if (file) command = command.concat(["--file", file])
    return command.concat(args)
  }

  function editTasks() {
    if (editorProcess.running) return
    root.close()
    root.actionError = ""
    var args = ["edit"]
    var editor = String(setting("editor", ""))
    if (editor) args = args.concat(["--editor", editor])
    editorProcess.command = helperCommand(args)
    editorProcess.running = true
  }

  IpcHandler {
    target: "martin.todo.editor"
    function open(): void { root.editTasks() }
  }

  function toggleTask(task) {
    if (actionProcess.running) return
    actionError = ""
    actionProcess.command = helperCommand(["toggle", String(task.line), String(task.etag), "--revision", String(task.revision)])
    actionProcess.running = true
  }

  function toggleSection(priority) {
    if (priority === "P0") return
    defaultExpansionPending = false
    var next = { P0: expanded.P0, P1: expanded.P1, P2: expanded.P2 }
    next[priority] = !next[priority]
    expanded = next
  }

  function defaultHeightLimit() {
    return popup.screenH > 0
      ? Math.min(Style.space(460), popup.screenH / 3, popup.availableCardHeight)
      : Style.space(460)
  }

  function fitDefaultSections() {
    if (!opened || !defaultExpansionPending) return
    expanded = ({ P0: true, P1: true, P2: true })
    Qt.callLater(function() {
      if (!root.opened || !root.defaultExpansionPending) return
      if (content.implicitHeight + popup.verticalContentInset <= root.defaultHeightLimit()) {
        root.defaultExpansionPending = false
        return
      }
      root.expanded = ({ P0: true, P1: true, P2: false })
      Qt.callLater(function() {
        if (!root.opened || !root.defaultExpansionPending) return
        if (content.implicitHeight + popup.verticalContentInset > root.defaultHeightLimit())
          root.expanded = ({ P0: true, P1: false, P2: false })
        root.defaultExpansionPending = false
      })
    })
  }

  onOpenedChanged: if (opened) {
    defaultExpansionPending = true
    expanded = ({ P0: true, P1: false, P2: false })
    refresh()
  } else {
    defaultExpansionPending = false
  }

  Timer {
    interval: 3000
    running: root.opened
    repeat: true
    onTriggered: root.refresh()
  }

  Process {
    id: loadProcess
    command: root.helperCommand(["list"])
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          root.sections = JSON.parse(text)
          if (!root.actionError) root.errorText = ""
          if (root.defaultExpansionPending) root.fitDefaultSections()
        } catch (error) {
          root.errorText = "Could not read tasks"
        }
      }
    }
    onExited: function(exitCode) {
      if (exitCode !== 0) root.errorText = "Could not read tasks"
    }
  }

  Process {
    id: actionProcess
    stderr: StdioCollector {
      waitForEnd: true
      onStreamFinished: root.actionError = String(text || "").trim()
    }
    onExited: function(exitCode) {
      if (exitCode !== 0) root.errorText = root.actionError || "Could not save task"
      root.refresh()
    }
  }

  Process {
    id: editorProcess
    stderr: StdioCollector {
      waitForEnd: true
      onStreamFinished: root.actionError = String(text || "").trim()
    }
    onExited: function(exitCode) {
      if (exitCode !== 0) root.errorText = root.actionError || "Could not open editor"
    }
  }

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "\uf0ae"
    tooltipText: "To-do · right-click to edit"
    onPressed: function(mouseButton) {
      if (mouseButton === Qt.RightButton) {
        root.editTasks()
      } else {
        root.toggle()
      }
    }
  }

  // For a side bar, place the anchor past the screen's lower edge so the
  // shared KeyboardPanel clamps this compact card to its bottom margin.
  Item {
    id: bottomPopupAnchor
    width: 1
    height: 1
    y: popup.screenH
    opacity: 0
  }

  KeyboardPanel {
    id: popup
    anchorItem: root.bar && (root.bar.position === "left" || root.bar.position === "right")
      ? bottomPopupAnchor : button
    owner: root
    bar: root.bar
    open: root.opened
    focusTarget: keyCatcher
    contentWidth: popup.fittedContentWidth(Style.space(320))
    contentHeight: popup.fittedContentHeight(content.implicitHeight, root.defaultHeightLimit())

    PanelKeyCatcher {
      id: keyCatcher
      anchors.fill: parent
      onCloseRequested: root.close()
      onTabRequested: function(direction) { root.switchPanel(direction) }

      Flickable {
        anchors.fill: parent
        contentWidth: width
        contentHeight: content.implicitHeight
        clip: true
        boundsBehavior: Flickable.StopAtBounds

        Column {
          id: content
          width: parent.width
          spacing: Style.space(9)

          Repeater {
            model: root.priorities

            Column {
              id: section
              required property string modelData
              readonly property string priority: modelData
              width: content.width
              spacing: Style.space(6)

              PanelSeparator {
                visible: section.priority !== "P0"
                foreground: root.ink
              }

              Item {
                width: section.width
                height: Style.space(24)

                Rectangle {
                  anchors.fill: parent
                  radius: Style.cornerRadius
                  color: headingHover.hovered ? root.hoverTint : "transparent"
                }
                Row {
                  anchors.left: parent.left
                  anchors.leftMargin: Style.space(4)
                  anchors.verticalCenter: parent.verticalCenter
                  spacing: Style.space(8)
                  PanelSectionHeader {
                    text: section.priority
                    foreground: root.ink
                    fontFamily: root.bar ? root.bar.fontFamily : Style.font.family
                  }
                  Text {
                    text: String(root.openCount(section.priority))
                    color: Color.muted
                    font.family: Style.font.family
                    font.pixelSize: Style.font.caption
                  }
                }
                Text {
                  anchors.right: parent.right
                  anchors.rightMargin: Style.space(5)
                  anchors.verticalCenter: parent.verticalCenter
                  text: root.expanded[section.priority] ? "▾" : "▸"
                  color: Color.muted
                  font.family: Style.font.family
                  font.pixelSize: Style.font.bodySmall
                }
                HoverHandler { id: headingHover }
                TapHandler { onTapped: root.toggleSection(section.priority) }
              }

              Repeater {
                model: root.expanded[section.priority] ? root.openItemsFor(section.priority) : []
                Item {
                  id: taskRow
                  required property var modelData
                  readonly property var task: modelData
                  width: section.width
                  height: Style.space(28)

                  Rectangle {
                    anchors.fill: parent
                    radius: Style.cornerRadius
                    color: hover.hovered ? root.hoverTint : "transparent"
                  }
                  Rectangle {
                    id: tick
                    width: Style.space(14)
                    height: width
                    radius: 0
                    anchors.left: parent.left
                    anchors.leftMargin: Style.space(4)
                    anchors.verticalCenter: parent.verticalCenter
                    color: taskRow.task.done ? root.ink : "transparent"
                    border.width: 1
                    border.color: taskRow.task.done ? root.ink : Color.muted
                    Text {
                      anchors.centerIn: parent
                      text: "✓"
                      visible: taskRow.task.done
                      color: Color.background
                      font.bold: true
                      font.pixelSize: Style.font.bodySmall
                    }
                  }
                  Text {
                    id: taskText
                    anchors.left: tick.right
                    anchors.leftMargin: Style.space(8)
                    anchors.right: parent.right
                    anchors.rightMargin: Style.space(4)
                    anchors.verticalCenter: parent.verticalCenter
                    text: String(taskRow.task.text || "")
                    color: taskRow.task.done ? Color.muted : root.ink
                    font.family: Style.font.family
                    font.pixelSize: Style.font.body
                    font.strikeout: taskRow.task.done
                    wrapMode: Text.NoWrap
                    elide: Text.ElideRight
                  }
                  HoverHandler { id: hover }
                  PanelToolTip {
                    visible: hover.hovered
                    text: String(taskRow.task.description || "").trim() || String(taskRow.task.text || "")
                    fontFamily: Style.font.family
                  }
                  TapHandler { onTapped: root.toggleTask(taskRow.task) }
                }
              }

              Text {
                visible: root.expanded[section.priority] && root.openItemsFor(section.priority).length === 0
                text: "No open tasks"
                color: Color.muted
                font.family: Style.font.family
                font.pixelSize: Style.font.bodySmall
                leftPadding: Style.space(4)
              }

            }
          }

          Text {
            visible: root.errorText !== ""
            text: root.errorText
            color: Color.urgent
            font.family: Style.font.family
            font.pixelSize: Style.font.bodySmall
            width: parent.width
            wrapMode: Text.Wrap
          }
        }
      }
    }
  }
}
