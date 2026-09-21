from pathlib import Path
import csv

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ModuleNotFoundError as error:
    raise SystemExit(
        "Missing Week 3 dependencies. Install them with: "
        "python3 -m pip install -r requirements.txt"
    ) from error


# ------------------------------------------------------------
# 1. FOLDER CONFIGURATION
# ------------------------------------------------------------

# Location of the current Python file
BASE_DIR = Path(__file__).resolve().parent

# Folder for the text documents
DOCUMENTS_FOLDER = BASE_DIR / "documents"

# Folder for generated results
RESULTS_FOLDER = BASE_DIR / "results"


# ------------------------------------------------------------
# 2. SAMPLE ONLINE-SOURCE DOCUMENTS
# ------------------------------------------------------------

sample_documents = {
    "document_1.txt": """
Title: Introduction to Artificial Intelligence
Source: IBM
URL: https://www.ibm.com/think/topics/artificial-intelligence

Artificial intelligence allows computers and machines to perform tasks
that normally require human intelligence. These tasks include learning,
problem solving, language understanding, decision making, and recognizing
patterns. Machine learning is a branch of artificial intelligence that
allows computer systems to learn from data. Deep learning uses artificial
neural networks to process large amounts of complex information.
Artificial intelligence is used in customer service, fraud detection,
recommendation systems, healthcare, education, and business automation.
""",

    "document_2.txt": """
Title: Artificial Intelligence Risk Management
Source: National Institute of Standards and Technology
URL: https://www.nist.gov/itl/ai-risk-management-framework

Artificial intelligence risk management helps organizations create and
use trustworthy AI systems. Organizations must identify possible risks
related to privacy, security, fairness, transparency, and reliability.
The NIST AI Risk Management Framework includes four main functions:
govern, map, measure, and manage. Governance defines responsibilities
and policies. Mapping identifies the context and possible effects of an
AI system. Measurement evaluates system performance and risk. Management
helps organizations prioritize and control the identified risks.
""",

    "document_3.txt": """
Title: Artificial Intelligence in Education
Source: UNESCO
URL: https://www.unesco.org/en/digital-education/artificial-intelligence

Artificial intelligence can improve education by supporting personalized
learning, automated feedback, and educational management. AI tools can
help teachers prepare lessons and allow students to access learning
materials based on their individual needs. However, educational
institutions must consider privacy, academic integrity, fairness, and
equal access. Teachers and students require AI literacy to understand
the benefits and limitations of automated systems. Artificial intelligence
should support teachers rather than completely replace human interaction.
""",

    "document_4.txt": """
Title: Artificial Intelligence in Healthcare
Source: World Health Organization
URL: https://www.who.int/publications/i/item/9789240029200

Artificial intelligence can support healthcare through medical image
analysis, clinical decision making, disease detection, patient monitoring,
and drug development. AI systems can help doctors analyze large amounts
of health information. However, inaccurate or biased systems may create
risks for patients. Healthcare organizations must protect patient privacy,
ensure cybersecurity, and test AI systems carefully. Human supervision,
transparency, accountability, and informed consent are important when
artificial intelligence is used in healthcare.
""",

    "document_5.txt": """
Title: Artificial Intelligence and Cybersecurity
Source: Cybersecurity and Infrastructure Security Agency
URL: https://www.cisa.gov/topics/cyber-threats-and-advisories/artificial-intelligence

Artificial intelligence is increasingly used in cybersecurity. Machine
learning can detect unusual network activity, malicious software, fraud,
and possible cyberattacks. Security teams can use AI to analyze alerts
and respond to incidents more quickly. However, attackers may also use
generative AI to produce phishing messages and automate cyberattacks.
Organizations should protect training data, control system access,
monitor AI applications, and maintain human review of important security
decisions.
""",

    "document_6.txt": """
Title: Artificial Intelligence in Earth Science
Source: NASA
URL: https://science.nasa.gov/earth-science/data/artificial-intelligence/

Satellites collect large amounts of information about the atmosphere,
oceans, forests, weather, and climate. Artificial intelligence and
machine learning can help scientists process satellite data and identify
important patterns. AI models can support the detection of floods,
wildfires, storms, and environmental changes. Scientists must use
reliable training data and carefully validate model predictions.
Artificial intelligence supports scientific analysis, but human knowledge
is still necessary for interpreting environmental information.
""",

    "document_7.txt": """
Title: Artificial Intelligence and Public Policy
Source: Organisation for Economic Co-operation and Development
URL: https://www.oecd.org/en/topics/artificial-intelligence.html

Artificial intelligence can improve productivity, scientific research,
public services, and economic development. Governments need policies
that encourage innovation while protecting privacy, security, fairness,
human rights, and democratic values. Responsible artificial intelligence
requires transparency, accountability, robustness, and human oversight.
Workers may require new skills as AI changes workplace activities.
International cooperation is also important because artificial
intelligence technologies and their risks can affect many countries.
""",

    "document_8.txt": """
Title: Artificial Intelligence and the Global Economy
Source: International Monetary Fund
URL: https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity

Artificial intelligence is expected to change employment and productivity
throughout the global economy. AI may help workers complete tasks,
analyze information, and make better decisions. However, automation may
reduce demand for some jobs and increase economic inequality. Governments
should invest in digital infrastructure, education, worker training,
social protection, and appropriate regulation. Public policy will
influence whether the economic benefits of artificial intelligence are
shared across workers, businesses, and countries.
"""
}


# ------------------------------------------------------------
# 3. CREATE REQUIRED FOLDERS AND DOCUMENTS
# ------------------------------------------------------------

def create_project_files():
    """
    Create the documents and results folders.

    The sample text documents are only created if they do not already
    exist. Therefore, existing documents will not be overwritten.
    """

    DOCUMENTS_FOLDER.mkdir(exist_ok=True)
    RESULTS_FOLDER.mkdir(exist_ok=True)

    for filename, content in sample_documents.items():
        file_path = DOCUMENTS_FOLDER / filename

        if not file_path.exists():
            file_path.write_text(
                content.strip(),
                encoding="utf-8"
            )

            print(f"Created: {filename}")
        else:
            print(f"Already exists: {filename}")


# ------------------------------------------------------------
# 4. LOAD THE DOCUMENTS
# ------------------------------------------------------------

def load_documents():
    """Read all text documents from the documents folder."""

    document_paths = sorted(
        DOCUMENTS_FOLDER.glob("*.txt")
    )

    if len(document_paths) < 5:
        raise ValueError(
            "At least five text documents are required."
        )

    document_names = []
    document_texts = []

    for path in document_paths:
        text = path.read_text(encoding="utf-8")

        document_names.append(path.stem)
        document_texts.append(text)

        print(f"Loaded: {path.name}")

    return document_names, document_texts


# ------------------------------------------------------------
# 5. CREATE TF-IDF VECTORS
# ------------------------------------------------------------

def create_tfidf_vectors(document_texts):
    """
    Convert all documents into TF-IDF vectors.

    Unigrams represent individual words.
    Bigrams represent two-word combinations.
    """

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        document_texts
    )

    return vectorizer, tfidf_matrix


# ------------------------------------------------------------
# 6. CALCULATE COSINE SIMILARITY
# ------------------------------------------------------------

def calculate_similarity(tfidf_matrix):
    """Calculate cosine similarity between every document."""

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    return similarity_matrix


# ------------------------------------------------------------
# 7. RANK DOCUMENT PAIRS
# ------------------------------------------------------------

def rank_document_pairs(
    document_names,
    similarity_matrix
):
    """
    Rank unique document pairs from highest to lowest similarity.

    Self-comparisons and duplicate pairs are excluded.
    """

    ranked_pairs = []

    number_of_documents = len(document_names)

    for first_index in range(number_of_documents):
        for second_index in range(
            first_index + 1,
            number_of_documents
        ):
            score = similarity_matrix[
                first_index,
                second_index
            ]

            ranked_pairs.append({
                "document_1": document_names[first_index],
                "document_2": document_names[second_index],
                "score": score
            })

    ranked_pairs.sort(
        key=lambda pair: pair["score"],
        reverse=True
    )

    return ranked_pairs


# ------------------------------------------------------------
# 8. DISPLAY THE SIMILARITY MATRIX
# ------------------------------------------------------------

def display_similarity_matrix(
    document_names,
    similarity_matrix
):
    """Print the complete similarity matrix."""

    short_names = [
        name.replace("document_", "D")
        for name in document_names
    ]

    print("\nSIMILARITY MATRIX")
    print("-" * 80)

    print(f"{'':8}", end="")

    for name in short_names:
        print(f"{name:>8}", end="")

    print()

    for row_index, row in enumerate(
        similarity_matrix
    ):
        print(f"{short_names[row_index]:8}", end="")

        for score in row:
            print(f"{score:8.4f}", end="")

        print()


# ------------------------------------------------------------
# 9. DISPLAY RANKED RESULTS
# ------------------------------------------------------------

def display_ranked_pairs(ranked_pairs):
    """Print all ranked document pairs."""

    print("\nRANKED DOCUMENT PAIRS")
    print("-" * 70)

    for rank, pair in enumerate(
        ranked_pairs,
        start=1
    ):
        first_document = pair[
            "document_1"
        ].replace("document_", "D")

        second_document = pair[
            "document_2"
        ].replace("document_", "D")

        print(
            f"{rank:>2}. "
            f"{first_document} and "
            f"{second_document} = "
            f"{pair['score']:.4f}"
        )


# ------------------------------------------------------------
# 10. SAVE SIMILARITY MATRIX AS CSV
# ------------------------------------------------------------

def save_similarity_matrix(
    document_names,
    similarity_matrix
):
    """Save the complete similarity matrix to a CSV file."""

    short_names = [
        name.replace("document_", "D")
        for name in document_names
    ]

    output_path = (
        RESULTS_FOLDER / "similarity_matrix.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(
            ["Document"] + short_names
        )

        for document_name, row in zip(
            short_names,
            similarity_matrix
        ):
            formatted_scores = [
                f"{score:.4f}"
                for score in row
            ]

            writer.writerow(
                [document_name] + formatted_scores
            )

    print(f"Saved: {output_path.name}")


# ------------------------------------------------------------
# 11. SAVE RANKED PAIRS AS CSV
# ------------------------------------------------------------

def save_ranked_pairs(ranked_pairs):
    """Save the ranked document pairs to a CSV file."""

    output_path = (
        RESULTS_FOLDER / "ranked_pairs.csv"
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "Rank",
            "Document 1",
            "Document 2",
            "Cosine Similarity"
        ])

        for rank, pair in enumerate(
            ranked_pairs,
            start=1
        ):
            writer.writerow([
                rank,
                pair["document_1"],
                pair["document_2"],
                f"{pair['score']:.4f}"
            ])

    print(f"Saved: {output_path.name}")


# ------------------------------------------------------------
# 12. CREATE SIMILARITY HEATMAP
# ------------------------------------------------------------

def create_heatmap(
    document_names,
    similarity_matrix
):
    """Create and save a document-similarity heatmap."""

    short_names = [
        name.replace("document_", "D")
        for name in document_names
    ]

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        similarity_matrix,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        xticklabels=short_names,
        yticklabels=short_names,
        vmin=0,
        vmax=1,
        square=True,
        cbar_kws={
            "label": "Cosine Similarity"
        }
    )

    plt.title(
        "Document Similarity Using TF-IDF and Cosine Similarity"
    )

    plt.xlabel("Documents")
    plt.ylabel("Documents")
    plt.tight_layout()

    output_path = (
        RESULTS_FOLDER / "similarity_heatmap.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Saved: {output_path.name}")
    # Avoid opening a GUI window so this also works in headless terminals.
    plt.close()


# ------------------------------------------------------------
# 13. MAIN FUNCTION
# ------------------------------------------------------------

def main():
    print("=" * 70)
    print("WEEK 3: DOCUMENT SIMILARITY USING VECTOR SPACE MODEL")
    print("=" * 70)

    # Create folders and sample documents
    create_project_files()

    # Load the documents
    document_names, document_texts = (
        load_documents()
    )

    # Create the TF-IDF matrix
    vectorizer, tfidf_matrix = (
        create_tfidf_vectors(document_texts)
    )

    # Calculate similarity
    similarity_matrix = calculate_similarity(
        tfidf_matrix
    )

    # Rank all unique document pairs
    ranked_pairs = rank_document_pairs(
        document_names,
        similarity_matrix
    )

    # Display project information
    print("\nPROJECT INFORMATION")
    print("-" * 70)
    print(
        f"Number of documents: "
        f"{len(document_names)}"
    )
    print(
        f"Number of TF-IDF features: "
        f"{len(vectorizer.get_feature_names_out())}"
    )
    print(
        f"TF-IDF matrix shape: "
        f"{tfidf_matrix.shape}"
    )
    print(
        f"Unique document pairs: "
        f"{len(ranked_pairs)}"
    )

    # Display the complete matrix
    display_similarity_matrix(
        document_names,
        similarity_matrix
    )

    # Display the ranked pairs
    display_ranked_pairs(ranked_pairs)

    # Display the most similar pair
    most_similar = ranked_pairs[0]

    print("\nMOST SIMILAR DOCUMENTS")
    print("-" * 70)
    print(
        f"First document: "
        f"{most_similar['document_1']}"
    )
    print(
        f"Second document: "
        f"{most_similar['document_2']}"
    )
    print(
        f"Cosine similarity: "
        f"{most_similar['score']:.4f}"
    )

    # Save all results
    print("\nSAVING RESULTS")
    print("-" * 70)

    save_similarity_matrix(
        document_names,
        similarity_matrix
    )

    save_ranked_pairs(ranked_pairs)

    create_heatmap(
        document_names,
        similarity_matrix
    )

    print("\nProgram completed successfully.")
    print(
        f"Documents folder: {DOCUMENTS_FOLDER}"
    )
    print(
        f"Results folder: {RESULTS_FOLDER}"
    )


# ------------------------------------------------------------
# 14. RUN THE PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
