import sys
import time
from dataclasses import dataclass
from typing import Optional, Callable

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QScrollArea, QLabel, QSizePolicy, QFrame, QFileDialog, QMessageBox, QToolButton, QMenu,
    QSplitter
)

# --------- Data model ---------
@dataclass
class ChatMessage:
    role: str              # "user" or "assistant"
    content: str


# --------- Message bubble widget ---------
class ChatBubble(QWidget):
    def __init__(self, msg: ChatMessage, parent=None):
        super().__init__(parent)
        self.msg = msg

        outer = QHBoxLayout(self)
        outer.setContentsMargins(8, 2, 8, 2)

        bubble = QFrame()
        bubble.setFrameShape(QFrame.Shape.NoFrame)
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        # Text
        text = QLabel(msg.content)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setWordWrap(True)
        text.setFont(QFont("Segoe UI", 10))

        # Role label
        role = QLabel("You" if msg.role == "user" else "Assistant")
        role.setFont(QFont("Segoe UI", 8, QFont.Weight.Medium))
        role.setStyleSheet("color: #666;")

        # Layout
        v = QVBoxLayout(bubble)
        v.setContentsMargins(14, 10, 14, 10)
        v.setSpacing(6)
        v.addWidget(role)
        v.addWidget(text)

        # Simple bubble styling
        if msg.role == "user":
            bubble.setStyleSheet("""
                QFrame { background: #d9f0ff; border-radius: 12px; }
                QLabel { color: #0a0a0a; }
            """)
            outer.addStretch()
            outer.addWidget(bubble, 0)
        else:
            bubble.setStyleSheet("""
                QFrame { background: #f4f4f5; border-radius: 12px; }
                QLabel { color: #0a0a0a; }
            """)
            outer.addWidget(bubble, 0)
            outer.addStretch()


# --------- Scrollable chat history ---------
class ChatHistory(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; }")

        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setContentsMargins(12, 12, 12, 12)
        self.vbox.setSpacing(8)
        self.vbox.addStretch()
        self.setWidget(self.container)

    def add_message(self, msg: ChatMessage):
        # Insert before the stretch
        stretch = self.vbox.itemAt(self.vbox.count() - 1)
        self.vbox.removeItem(stretch)
        self.vbox.addWidget(ChatBubble(msg))
        self.vbox.addItem(stretch)
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        QApplication.processEvents()
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


# --------- Background worker (plug in your backend here) ---------
class BackendWorker(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt: str, backend_fn: Optional[Callable[[str], str]] = None):
        super().__init__()
        self.prompt = prompt
        self.backend_fn = backend_fn

    def run(self):
        try:
            if self.backend_fn:
                # Call your real backend (e.g., LLM API) here
                reply = self.backend_fn(self.prompt)
            else:
                # Demo fallback: "typing…" then a simple echo/transform
                time.sleep(0.8)
                reply = f"You said: {self.prompt.strip()}\n\n(Replace backend_fn to call your model/API.)"
            self.result.emit(reply)
        except Exception as e:
            self.error.emit(str(e))


# --------- Main window ---------
class ChatWindow(QWidget):
    def __init__(self, backend_fn: Optional[Callable[[str], str]] = None):
        super().__init__()
        self.backend_fn = backend_fn
        self.setWindowTitle("Knowledge Engine ChatBot")
        self.setMinimumSize(QSize(800, 540))

        # Top bar
        topbar = self._build_topbar()

        # Chat history
        self.history = ChatHistory()

        # Input area
        self.input = QTextEdit()
        self.input.setPlaceholderText("Send a message…")
        self.input.setFont(QFont("Segoe UI", 10))
        self.input.setFixedHeight(90)
        self.input.installEventFilter(self)

        self.send_btn = QPushButton("Send")
        self.send_btn.setDefault(True)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.on_send)

        input_row = QHBoxLayout()
        input_row.addWidget(self.input, 1)
        input_row.addWidget(self.send_btn)

        # Splitter for future extensibility (e.g., right panel for settings/history)
        center = QSplitter(Qt.Orientation.Horizontal)
        center.addWidget(self.history)
        right_stub = QWidget()
        right_stub.setMinimumWidth(0)
        center.addWidget(right_stub)
        center.setSizes([1000, 0])

        # Root layout
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)
        root.addLayout(topbar)
        root.addWidget(center, 1)
        root.addLayout(input_row)

        self.setStyleSheet("""
            QWidget { background: #ffffff; }
            QPushButton {
                background: #111827; color: white; border: none; padding: 10px 16px; border-radius: 10px;
            }
            QPushButton:hover { background: #0b1220; }
            QTextEdit {
                background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px;
            }
        """)

        # Greet message
        self.history.add_message(ChatMessage("assistant", "Hi! Ask me anything."))

    def _build_topbar(self) -> QHBoxLayout:
        title = QLabel("ChatBot")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))

        # Menu (export / clear)
        menu_btn = QToolButton()
        menu_btn.setText("⋯")
        menu_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        menu = QMenu(menu_btn)
        act_save = QAction("Export conversation…", self)
        act_clear = QAction("Clear conversation", self)
        act_save.triggered.connect(self.export_conversation)
        act_clear.triggered.connect(self.clear_conversation)
        menu.addAction(act_save)
        menu.addAction(act_clear)
        menu_btn.setMenu(menu)
        menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        hb = QHBoxLayout()
        hb.setContentsMargins(4, 4, 4, 4)
        hb.addWidget(title)
        hb.addStretch()
        hb.addWidget(menu_btn)
        return hb

    def eventFilter(self, obj, event):
        # Enter to send, Shift+Enter for newline
        if obj is self.input and event.type().name == "KeyPress":
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    return False  # allow newline
                self.on_send()
                return True
        return super().eventFilter(obj, event)

    def on_send(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        self.input.clear()

        # Add user message
        self.history.add_message(ChatMessage("user", text))

        # Add placeholder "assistant is typing…" bubble
        typing_msg = ChatMessage("assistant", "…")
        self.history.add_message(typing_msg)

        # Kick off worker
        self.worker = BackendWorker(text, backend_fn=self.backend_fn)
        self.worker.result.connect(lambda r: self._replace_last_assistant(r))
        self.worker.error.connect(lambda e: self._replace_last_assistant(f"Error: {e}"))
        self.worker.start()

    def _replace_last_assistant(self, new_text: str):
        # Replace the last assistant bubble content
        layout = self.history.vbox
        # last widget is stretch; one before may be bubble; scan backwards
        for i in range(layout.count() - 2, -1, -1):
            item = layout.itemAt(i)
            w = item.widget()
            if isinstance(w, ChatBubble) and w.msg.role == "assistant":
                w.msg.content = new_text
                # update label text
                label = w.findChildren(QLabel)[1]  # role label is [0], text is [1]
                label.setText(new_text)
                self.history._scroll_to_bottom()
                return

    def export_conversation(self):
        # Simple plaintext export
        path, _ = QFileDialog.getSaveFileName(self, "Export conversation", "conversation.txt", "Text Files (*.txt)")
        if not path:
            return
        try:
            lines = []
            layout = self.history.vbox
            for i in range(layout.count() - 1):  # skip stretch
                w = layout.itemAt(i).widget()
                if isinstance(w, ChatBubble):
                    lines.append(f"{'You' if w.msg.role=='user' else 'Assistant'}:\n{w.msg.content}\n")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            QMessageBox.information(self, "Exported", f"Saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_conversation(self):
        # Clear all bubbles
        layout = self.history.vbox
        for i in reversed(range(layout.count() - 1)):  # keep stretch
            item = layout.itemAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
        self.history.add_message(ChatMessage("assistant", "Conversation cleared. How can I help?"))


# --------- Optional: example backend function ---------
def demo_backend(prompt: str) -> str:
    """Replace this with your real LLM/API call."""
    # Simulate some thinking
    time.sleep(0.6)
    # A tiny canned behavior
    if prompt.lower().startswith("help"):
        return "Sure! Ask a question or describe a task, and I’ll respond."
    return f"Echo: {prompt}\n\n(Implement your API call in demo_backend.)"


# --------- Main ---------
def main():
    app = QApplication(sys.argv)
    # Pass None to use the built-in demo fallback; pass demo_backend to see the hook in action
    w = ChatWindow(backend_fn=demo_backend)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
