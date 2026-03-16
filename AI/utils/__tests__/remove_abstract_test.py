import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from remove_abstract import remove_abstract

test_cases = [
{
"title": "empty text",
"text": "",
"abstract": "Some abstract text.",
"expected": ""
},

{
"title": "empty abstract",
"text": "Paper Title\nIntroduction starts here.",
"abstract": "",
"expected": "Paper Title\nIntroduction starts here."
},

{
"title": "empty text and abstract",
"text": "",
"abstract": "",
"expected": ""
},

{
"title": "exact abstract removal",
"text": (
    "Paper Title\n"
    "This paper studies machine learning models and their performance.\n"
    "Introduction section starts here."
),
"abstract": "This paper studies machine learning models and their performance.",
"expected": "Paper Title\n\nIntroduction section starts here."
},

 {
 "title": "no abstract present",
 "text": (
     "Paper Title\n"
     "Introduction begins immediately.\n"
     "More content follows."
 ),
 "abstract": "This abstract does not exist in the text.",
 "expected": "Paper Title\nIntroduction begins immediately.\nMore content follows."
 },
 
 {
 "title": "multiple occurrences only first removed",
 "text": (
     "Title\n"
     "This abstract text appears here.\n"
     "Introduction begins.\n"
     "Later we repeat: This abstract text appears here."
 ),
 "abstract": "This abstract text appears here.",
 "expected": (
     "Title\n\nIntroduction begins.\nLater we repeat: This abstract text appears here."
 )
 },
{
    "title": "real paper abstract removal",
    "text": """# Uncovering Locally Low-dimensional Structure in Networks by Locally Optimal Spectral Embedding

# Abstract

Standard Adjacency Spectral Embedding (ASE) relies on a global low-rank assumption often incompatible with the sparse, transitive structure of real-world networks, causing local geometric features to be 'smeared'. To address this, we introduce Local Adjacency Spectral Embedding (LASE), which uncovers locally low-dimensional structure via weighted spectral decomposition. Under a latent position model with a kernel feature map, we treat the image of latent positions as a locally low-dimensional set in infinite-dimensional feature space.

Keywords: spectral embedding, graph representation learning, manifold learning

# 1 Introduction

Spectral embedding provides a reformulation and generalisation of PCA for dimension reduction.
""",
    "abstract": (
        "Standard Adjacency Spectral Embedding (ASE) relies on a global low-rank assumption "
        "often incompatible with the sparse, transitive structure of real-world networks, "
        "causing local geometric features to be 'smeared'. To address this, we introduce "
        "Local Adjacency Spectral Embedding (LASE), which uncovers locally low-dimensional "
        "structure via weighted spectral decomposition. Under a latent position model with "
        "a kernel feature map, we treat the image of latent positions as a locally low-dimensional "
        "set in infinite-dimensional feature space."
    ),
    "expected": """# Uncovering Locally Low-dimensional Structure in Networks by Locally Optimal Spectral Embedding

# Abstract



Keywords: spectral embedding, graph representation learning, manifold learning

# 1 Introduction

Spectral embedding provides a reformulation and generalisation of PCA for dimension reduction.
"""
},
{
    "title": "similar abstract removal",
    "text": (
        "Title\n"
        "This research investigates neural networks for image classification in large datasets.\n"
        "The introduction begins here.\n"
        "This research investigates neural networks for image classification in large datasets.\n"
    ),
    "abstract": "This research investigates neural networks for image classification.",
    "expected": "Title in large datasets.\nThe introduction begins here.\nThis research investigates neural networks for image classification in large datasets.\n"
},
{
    "title": "abstract removal with typos - threshold test",
    "text": (
        "Paper Title\n"
        "This paper studdies machine learning models and their performence.\n"
        "Introduction section starts here."
    ),
    "abstract": "This paper studies machine learning models and their performance.",
    "expected": "Paper Title\n.\nIntroduction section starts here."
},
{
    "title": "very long scientific paper abstract removal",
    "text": """Deep Learning Approaches for Predicting Protein Structure

# Abstract

Predicting the three-dimensional structure of proteins from their amino acid sequences remains one of the fundamental challenges in computational biology. Recent advances in deep learning, particularly in the use of attention mechanisms and graph neural networks, have enabled models to capture long-range dependencies in sequences, thereby improving the accuracy of structure prediction. In this work, we present a novel neural architecture that integrates sequence-based embeddings with evolutionary information to predict both local and global structural features. Our method demonstrates state-of-the-art performance on benchmark datasets and provides insights into the interpretability of deep learning models in structural biology.

We further explore the integration of multiple sequence alignments (MSAs) and structural templates, which allow our model to leverage homologous sequences and structural priors. Extensive ablation studies confirm that each component contributes significantly to the predictive performance. Additionally, we analyze model uncertainty and highlight cases where prediction confidence correlates with experimental validation. Finally, we provide a discussion of computational efficiency and scalability, demonstrating that our approach can process large protein families in reasonable timeframes.

# 1 Introduction

Proteins are essential biomolecules that perform a vast array of functions in living organisms. Understanding their three-dimensional structure is crucial for applications ranging from drug discovery to enzyme engineering. Traditional experimental methods such as X-ray crystallography and NMR spectroscopy are labor-intensive and time-consuming, which motivates the development of computational prediction methods.

Recent computational approaches leverage deep learning to capture complex dependencies within protein sequences. Models such as AlphaFold have demonstrated remarkable success, yet challenges remain in modeling rare protein families, multi-domain proteins, and intrinsically disordered regions. Our proposed method extends prior work by combining sequence embeddings, evolutionary information, and graph-based representations to improve prediction across a wider range of proteins. We also discuss interpretability techniques to understand which sequence features drive structural predictions.

In the following sections, we describe the dataset preparation, model architecture, training procedure, and evaluation metrics. We then present results on benchmark datasets, compare with state-of-the-art methods, and perform detailed case studies highlighting both successes and limitations. Finally, we conclude with future directions and potential applications in computational biology and drug discovery.
""",
    "abstract": (
        "Predicting the three-dimensional structure of proteins from their amino acid sequences remains one of the fundamental challenges in computational biology. "
        "Recent advances in deep learning, particularly in the use of attention mechanisms and graph neural networks, have enabled models to capture long-range dependencies in sequences, thereby improving the accuracy of structure prediction. "
        "In this work, we present a novel neural architecture that integrates sequence-based embeddings with evolutionary information to predict both local and global structural features. "
        "Our method demonstrates state-of-the-art performance on benchmark datasets and provides insights into the interpretability of deep learning models in structural biology. "
        "We further explore the integration of multiple sequence alignments (MSAs) and structural templates, which allow our model to leverage homologous sequences and structural priors. "
        "Extensive ablation studies confirm that each component contributes significantly to the predictive performance. "
        "Additionally, we analyze model uncertainty and highlight cases where prediction confidence correlates with experimental validation. "
        "Finally, we provide a discussion of computational efficiency and scalability, demonstrating that our approach can process large protein families in reasonable timeframes."
    ),
    "expected": """Deep Learning Approaches for Predicting Protein Structure

# Abstract

.

# 1 Introduction

Proteins are essential biomolecules that perform a vast array of functions in living organisms. Understanding their three-dimensional structure is crucial for applications ranging from drug discovery to enzyme engineering. Traditional experimental methods such as X-ray crystallography and NMR spectroscopy are labor-intensive and time-consuming, which motivates the development of computational prediction methods.

Recent computational approaches leverage deep learning to capture complex dependencies within protein sequences. Models such as AlphaFold have demonstrated remarkable success, yet challenges remain in modeling rare protein families, multi-domain proteins, and intrinsically disordered regions. Our proposed method extends prior work by combining sequence embeddings, evolutionary information, and graph-based representations to improve prediction across a wider range of proteins. We also discuss interpretability techniques to understand which sequence features drive structural predictions.

In the following sections, we describe the dataset preparation, model architecture, training procedure, and evaluation metrics. We then present results on benchmark datasets, compare with state-of-the-art methods, and perform detailed case studies highlighting both successes and limitations. Finally, we conclude with future directions and potential applications in computational biology and drug discovery.
"""
}

]
 
 
@pytest.mark.parametrize("case", test_cases, ids=[c["title"] for c in test_cases])
def test_remove_abstract_cases(case):

    result = remove_abstract(case["text"], case["abstract"])

    print(f"result: {result}")


    assert result == case["expected"]