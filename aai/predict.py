import os
import graphviz
import pandas
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split

lookup = {9000: "United_States", 1000: "France", 2000: "Italy", 3000: "Netherlands", 4000: "Russia",
          5000: "United_Kingdom", 6000: "England", 7000: "Spain", 8000: "Australia", 1: "Modernism",
          2: "Post-Impressionism", 3: "Impressionism", 4: "Gothic_art", 5: "Baroque", 6: "Dutch_Golden_Age_painting",
          7: "Romanticism", 8: "Surrealism", 9: "Realism_(arts)", 10: "Minimalism", 11: "Sienese_School",
          12: "Classicism", 13: "Regionalism_(art)", 14: "Cubism", 15: "Dada", 16: "Fauvism",
          17: "Pre-Raphaelite_Brotherhood", 18: "Arts_and_Crafts_movement", 19: "Aestheticism", 20: "Abstract"}
inv_lookup = {v: k for k, v in lookup.items()}

dataset = pandas.read_csv("data/InputFile.csv")
print(dataset)
X = dataset.drop('movement', axis=1)
X = X.drop('Unnamed: 3', axis=1)
y = dataset['movement']

classifier = DecisionTreeClassifier()
classifier.fit(X, y)


def test_and_visualize():
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    classifier = DecisionTreeClassifier()
    classifier.fit(x_train, y_train)

    y_pred = classifier.predict(x_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    dot_data = export_graphviz(classifier, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("classifier")


def predict_movement(location, year):
    try:
        loc = inv_lookup[location]
    except KeyError:
        loc = 1111
    mov = classifier.predict([[loc, year]])
    return lookup[int(mov)]
