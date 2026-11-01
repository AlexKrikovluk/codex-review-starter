import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('Codex Review Alerts is now active');

  const runReviewCommand = vscode.commands.registerCommand('codexReview.runReview', () => {
    vscode.window.showInformationMessage('Running Codex review...');
  });

  const showHistoryCommand = vscode.commands.registerCommand('codexReview.showHistory', () => {
    vscode.window.showInformationMessage('Review history coming soon');
  });

  context.subscriptions.push(runReviewCommand, showHistoryCommand);
}

export function deactivate() {}
