from metaflow import FlowSpec, step
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

class WineAblationFlow(FlowSpec):

    @step
    def start(self):
        """
        This is the start step of the flow.
        """
        print("Starting the wine dataset ablation study flow.")
        self.next(self.load_data)

    @step
    def load_data(self):
        """
        Load the wine dataset.
        """
        print("Loading wine dataset...")
        data = load_wine()
        X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
        
        # Standardize the data
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(X_train)
        self.X_test = scaler.transform(X_test)
        self.y_train = y_train
        self.y_test = y_test
        
        self.next(self.train_logistic_regression, self.train_random_forest, self.train_svc)

    @step
    def train_logistic_regression(self):
        """
        Train a Logistic Regression model.
        """
        print("Training Logistic Regression model...")
        model = LogisticRegression(max_iter=1000)
        model.fit(self.X_train, self.y_train)
        self.logistic_regression_accuracy = accuracy_score(self.y_test, model.predict(self.X_test))
        self.next(self.join)

    @step
    def train_random_forest(self):
        """
        Train a Random Forest model.
        """
        print("Training Random Forest model...")
        model = RandomForestClassifier()
        model.fit(self.X_train, self.y_train)
        self.random_forest_accuracy = accuracy_score(self.y_test, model.predict(self.X_test))
        self.next(self.join)

    @step
    def train_svc(self):
        """
        Train a Support Vector Classifier model.
        """
        print("Training Support Vector Classifier model...")
        model = SVC()
        model.fit(self.X_train, self.y_train)
        self.svc_accuracy = accuracy_score(self.y_test, model.predict(self.X_test))
        self.next(self.join)

    @step
    def join(self, inputs):
        """
        Join the results from different models.
        """
        self.logistic_regression_accuracy = inputs.train_logistic_regression.logistic_regression_accuracy
        self.random_forest_accuracy = inputs.train_random_forest.random_forest_accuracy
        self.svc_accuracy = inputs.train_svc.svc_accuracy
        self.next(self.end)

    @step
    def end(self):
        """
        End of the flow.
        """
        print("Ablation study completed.")
        print(f"Logistic Regression Accuracy: {self.logistic_regression_accuracy}")
        print(f"Random Forest Accuracy: {self.random_forest_accuracy}")
        print(f"SVC Accuracy: {self.svc_accuracy}")

if __name__ == '__main__':
    WineAblationFlow()

    