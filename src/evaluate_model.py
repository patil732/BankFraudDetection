import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class ModelEvaluator:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

    def plot_confusion_matrix(self, cm, save_path=None, show=True):
        """Plot enhanced confusion matrix"""
        labels = ['Non-Fraud', 'Fraud']

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='RdYlGn',
            xticklabels=labels,
            yticklabels=labels,
            linewidths=1,
            linecolor='black',
            cbar=False
        )

        cm_percent = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis] * 100

        for i in range(2):
            for j in range(2):
                ax.text(
                    j + 0.5,
                    i + 0.7,
                    f"({cm_percent[i, j]:.1f}%)",
                    ha="center",
                    va="center",
                    fontsize=11,
                    color="blue"
                )

        accuracy = np.trace(cm) / np.sum(cm)

        plt.title("Confusion Matrix - Fraud Detection", fontsize=16, fontweight="bold")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")

        plt.figtext(
            0.5,
            0.01,
            f"Accuracy: {accuracy:.2%}",
            ha="center",
            fontsize=12,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5)
        )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Confusion matrix saved to: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_feature_importance(
        self,
        importances,
        feature_names,
        save_path=None,
        top_n=20,
        show=True
    ):
        """Plot feature importance for tree-based models"""

        if importances is None or feature_names is None:
            print("⚠️ Feature importance not available.")
            return

        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False)

        importance_df = importance_df.head(top_n)

        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=importance_df,
            x="importance",
            y="feature",
            palette="viridis"
        )

        plt.title("Top Feature Importances", fontsize=14, fontweight="bold")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Feature importance plot saved to: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()
