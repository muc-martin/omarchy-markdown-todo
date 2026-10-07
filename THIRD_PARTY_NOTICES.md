# Source and license notices

The owner selected MIT for the original To-do code on October 7, 2026.
The CLI, tests, examples and agent skill were developed for a personal setup.
Later changes adjusted the panel's behavior and appearance. The available
history alone does not establish the provenance of every earlier code pattern.

The panel uses Omarchy patterns for the panel lifecycle, BarIconButton,
KeyboardPanel, PanelKeyCatcher, sections and theme values. Omarchy's MIT notice
is retained in the package. The components themselves are imported at runtime
and are not bundled.

Sources reviewed on October 7, 2026:

- https://github.com/omacom/omarchy/blob/quattro/LICENSE
- https://github.com/omacom/omarchy/tree/quattro/shell/Ui
- https://github.com/omacom/omarchy/tree/quattro/shell/plugins/panels/network

Python 3, QtQuick and Quickshell remain external runtime dependencies. The
package contains no copied libraries, fonts, icons or image files. The bar icon
is a character rendered with the font supplied by the Omarchy theme.
