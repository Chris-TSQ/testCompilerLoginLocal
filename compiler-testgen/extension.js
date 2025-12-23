const vscode = require("vscode");
const CompilerTestGenPlugin = require("./src/compiler-testgen-plugin");

function activate(context) {
  const disposable = vscode.commands.registerCommand(
    "testgen.generate",
    () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;

      const filePath = editor.document.fileName;
      new CompilerTestGenPlugin().run(filePath);

      vscode.window.showInformationMessage(
        "Unit tests generated successfully!"
      );
    }
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
