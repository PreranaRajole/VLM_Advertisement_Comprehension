# VLM Advertisement Comprehension: Dual-Task Evaluation Framework

**A comprehensive evaluation of Vision Language Models' ability to understand and interpret advertising content across comprehension and generation tasks.**

## 🔬 Research Overview

This project investigates how state-of-the-art Vision Language Models process advertisement imagery through a novel dual-task evaluation framework. We systematically analyze model performance across multiple comprehension scenarios and caption generation tasks, revealing critical limitations in current VLM architectures.

### Key Research Questions
- How do leading VLMs compare in advertisement comprehension tasks?
- What is the impact of textual information removal on model performance?
- Can VLMs generate meaningful advertisement descriptions from visual cues alone?
- What systematic biases exist in VLM advertisement interpretation?

## 📊 Key Findings

### Model Performance Hierarchy
- **LlaVA-Next**: 94-98% accuracy (best performer)
- **Qwen2.5**: 70-85% accuracy 
- **LlaVA-OneVision**: 70-85% accuracy

### Critical Discoveries
- **Text Dependency**: 15-25% performance drop when text removed from images
- **Symbol Blindness**: 0% success rate incorporating numerical data, icons, or technical specifications
- **Background Interpretation Gap**: 57.5% failure rate in contextual visual understanding
- **Systematic Confusion Patterns**: Car↔Bike, Air Conditioner↔Air Purifier

## 🎯 Methodology

#### Task 1: Multiple Choice Comprehension
- **Dataset**: 350 annotated advertisements (90% inter-coder reliability)
- **Test Cases**: 4 conditions with strategically designed distractors
  - Case 1: Original image, 5 options (including similar product confusion)
  - Case 2: Original image, 4 options (category-level discrimination)
  - Case 3: Text-removed image, 5 options (visual-only comprehension)
  - Case 4: Text-removed image, 4 options (visual-category discrimination)

#### Task 2: Caption Generation
- **Models**: LlaVA-Next with systematic prompt engineering
- **Evaluation Metrics**: BERT, BLEU, CIDEr, ROUGE, CLIP Score, CAPTURE
- **Prompt Hierarchy**: General description > Advertisement-aware > Advertisement-aware & Product-specific>

### Experimental Design
```
Models Tested: LlaVA-Next, LlaVA-OneVision, Qwen2.5
Evaluation Framework:
├── MCQ Tasks (All Models)
└── Generation Tasks (LlaVA-Next)
    ├── Multi-metric evaluation
    ├── Human assessment (5 categories)
    └── Prompt optimization
```

## 📈 Results Summary

### MCQ Task Performance

| Model | Case 1 | Case 2 | Case 3 | Case 4 |
|-------|--------|--------|--------|--------|
| LlaVA-Next | 18 mismatches | 6 mismatches | 55 mismatches | 31 mismatches |
| Qwen2.5 | 64 mismatches | 55 mismatches | 67 mismatches | 48 mismatches |
| LlaVA-OneVision | 68 mismatches | 57 mismatches | 70 mismatches | 53 mismatches |

### Generation Task Performance

| Metric | Overall Performance |
|--------|-------------------|
| Product Identification | 100% success |
| Caption Similarity | 55% yes, 27.5% partial, 17.5% no |
| Background Interpretation | 27.5% yes, 15% partial, 57.5% no |
| Audience Appropriateness | 60% yes, 17.5% partial, 22.5% no |
| Product Feature Identification | 40% yes, 22.5% partial, 37.5% no |

### Systematic Error Patterns

#### Most Common Confusions
1. **Car → Bike**: 4-7 instances per model
2. **Air Conditioner → Air Purifier**: 3-4 instances per model  
3. **Mobile → Laptop**: 2-3 instances per model
4. **Services → Automobiles**: Cross-category misclassification

#### Category-Specific Challenges
- **Transportation**: Persistent vehicle type confusion
- **Home Appliances**: Functional similarity leading to errors
- **Electronics**: Form factor-based misclassification
- **Services**: High cross-category error rates

## 🔍 Novel Contributions
- Systematic dual-task evaluation in advertisement domain
- Controlled experimental design with text presence/absence conditions
- Multi-metric assessment combining accuracy and generation quality
- Quantified text dependency in commercial VLM applications
- Identified specific failure modes for advertising technology

## 📁 Repository Structure

```
vlm-advertisement-comprehension/
├── README.md
├── data/
│   ├── annotations/
│   │   ├── selling_points_category_350.xlsx
│   │   └── annotation_guidelines.md
│   ├── images/
│   │   ├── original/
│   │   └── text_removed/
│   └── synthetic/
├── experiments/
│   ├── mcq_evaluation/
│   │   ├── case1_original_5option.py
│   │   ├── case2_original_4option.py
│   │   ├── case3_modified_5option.py
│   │   └── case4_modified_4option.py
│   ├── generation_evaluation/
│   │   ├── prompt_engineering/
│   │   ├── evaluation_metrics.py
│   │   └── human_assessment.py
│   └── synthetic_preference/
│       └── human_vs_ai_evaluation.py
├── models/
│   ├── llava_next/
│   ├── llava_onevision/
│   └── qwen2_5/
├── results/
│   ├── mcq_results/
│   ├── generation_results/
│   └── statistical_analysis/
├── analysis/
│   ├── error_pattern_analysis.ipynb
│   ├── inter_coder_reliability.ipynb
│   ├── performance_comparison.ipynb
│   └── prompt_optimization_analysis.ipynb
├── docs/
│   ├── methodology.md
│   ├── experimental_protocol.md
│   └── evaluation_metrics.md
└── requirements.txt
```

## 📊 Detailed Results

### Performance Analysis by Category

#### High-Performing Categories
- **Air Conditioner/Purifier**: Strong product identification but confusion between similar appliances
- **Baby Products**: 100% product identification, 66.7% caption accuracy
- **Sports Equipment**: Generally performed well with minimal background elements

#### Challenging Categories  
- **Bike/Car**: 0% caption similarity for bikes, systematic transportation confusion
- **Services**: High cross-category misidentification (→ Automobiles, Electronics)
- **Complex Backgrounds**: Failed to incorporate logos, design elements, contextual information

### Prompt Engineering Results

| Prompt Type | BERT F1 | CLIP Score | Background Interpretation |
|-------------|---------|------------|-------------------------|
| Product-Specific (P3V1) | 0.4811 | 0.72-0.94 | 27.5% success |
| Advertisement-Aware (P2V1) | 0.4682 | 0.8712 | 5.9% success |
| General Description (P1V1) | 0.4811* | 0.72-0.94* | 54.3% success |

## 🔬 Research Impact
- Novel benchmark for advertisement VLM evaluation
- Systematic methodology for dual-task assessment
- Evidence of critical limitations in current VLM architectures
- Identified specific failure modes for advertising AI applications
- Quantified text dependency in commercial VLM deployments
- Provided evidence-based recommendations for model improvement

### Future Research Directions
- Improving background context interpretation
- Developing advertisement-specific VLM architectures to detect symbols in the advertisments

## 👥 Team & Acknowledgments

**Research Team:**
- **Research carried out under the guidance of Prof. Ming Jiang
- **Collaborated with 4 members

---

*This research project demonstrates systematic evaluation of Vision Language Models in the advertisement domain, revealing critical limitations and providing evidence-based insights for future development.*
