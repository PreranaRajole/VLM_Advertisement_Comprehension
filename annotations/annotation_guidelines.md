# Advertisement Annotation Guidelines

## Overview

This document provides comprehensive guidelines for annotating advertisement images in the VLM Advertisement Comprehension dataset. These guidelines ensure consistency, quality, and reliability across all annotators.

**Target**: 90% inter-annotator agreement
**Team Size**: 4 annotators
**Dataset Size**: 350+ advertisement images

---

## 📋 Annotation Schema

Each advertisement must be annotated with the following five core dimensions:

### 1. **Product Name** 
*The specific product being advertised*

### 2. **Product Category**
*Primary classification from predefined categories*

### 3. **Selling Points**
*Key value propositions and benefits highlighted in the advertisement*

### 4. **Advertisement Caption**
*Human-generated caption of the advertisement's content*

### 5. **Extracted Text File**
*Clean text content from the advertisement (product-descriptive text only)*

---

## 🎯 Detailed Annotation Instructions

### 1. Product Name Annotation

#### Definition
The specific product, service, or brand being advertised. This should be the main focus of the advertisement.

#### Edge Cases
- **Multiple Products**: If multiple products shown, select the primary/dominant one
- **Unclear Products**: Use most specific identifiable term

---

### 2. Product Category Classification

#### Predefined Categories
1. **Electronics** (mobiles, laptops, TVs, audio devices)
2. **Home Appliances** (AC, refrigerator, washing machine, air purifier)
3. **Automobiles** (cars, bikes, scooters, commercial vehicles)
4. **Services** (banking, insurance, telecommunications, logistics)
5. **Self Care & Wellness** (soaps, shampoo, skincare, baby products, fitness)
6. **Food & Beverages** (snacks, drinks, dairy, restaurants)
7. **Finance** (banks, insurance, investment, loans)
8. **Travel & Tourism** (airlines, hotels, booking platforms)
9. **Accessories** (jewelry, watches, bags, fashion accessories)
10. **Clothes** (apparel, footwear, fashion brands)
11. **Home Essentials** (cleaning products, detergents, home care)

#### Classification Rules
- **Primary Purpose**: Choose based on the main function/use of the product
- **Single Category**: Each product gets exactly one primary category
- **Hierarchy**: When uncertain, use the more specific category
- **Service vs Product**: Services take precedence (e.g., "Bank Loan" = Finance, not Services)

#### Examples
✅ **Correct Classifications**:
- iPhone 15 → Electronics
- Hero Honda Bike → Automobiles  
- ICICI Personal Loan → Finance
- Dove Baby Shampoo → Self Care & Wellness
- McDonald's Burger → Food & Beverages

❌ **Common Mistakes**:
- Bank Advertisement → Finance (not Services)
- Fashion Jewelry → Accessories (not Clothes)
- Smartphone Accessory → Accessories (not Electronics)

---

### 3. Selling Points Annotation

#### Definition
The key value propositions, benefits, or features that the advertisement emphasizes to persuade consumers.

#### Identification Strategy
1. **Look for explicit claims** (text overlays, slogans, feature lists)
2. **Consider target audience** (professionals, families, young adults)
3. **Note emotional appeals** (happiness, security, status)

#### Format Requirements
- **Semi-colon Seperated Phrases**: Use ; to seperate multiple selling points
- **Concise Phrases**: 3-10 words per selling point
- **Complete Thoughts**: Each point should be independently meaningful


#### Examples

**Air Conditioner Advertisement**:
✅ **Good Selling Points**:
- Energy efficient cooling; Silent operation technology; 5-star rating; Fast cooling in 30 seconds; Affordable EMI options

❌ **Bad Selling Points**:
- "Good product" (too vague)
- "Nice looking" (not specific)
- "Cools air" (obvious function)


#### Edge Cases
- **Implicit Selling Points**: Include obvious implications (luxury car → status symbol)
- **Visual-Only Ads**: All ads considered had at least two selling points (phrases)
- **Multilingual Ads**: All ads considered were English
- **Celebrity Endorsements**: Exclude celebrity name until included in text

---

### 4. Advertisement Caption/Description

#### Purpose
human-readable description that captures the advertisement's message, mood, and content all taken directly from the text for comparison with AI-generated captions.

#### Length Guidelines
- **Target Length**:  More than 5 words
- **Maximum**: One or two lines

---

## 🔍 Quality Control Procedures

### Inter-Annotator Agreement Process

#### Initial Calibration
1. **Training Set**: All annotators practice on 20 sample images
2. **Discussion**: Resolve disagreements and clarify guidelines
3. **Test Set**: Annotate 30 images independently
4. **Agreement Check**: Calculate agreement percentage

#### Ongoing Validation
1. **Validation Subset**: 110 images (31.4% of dataset) annotated by multiple annotators
2. **Agreement Threshold**: Minimum 90% agreement required
3. **Disagreement Resolution**: Systematic process for conflicts
4. **Regular Calibration**: Monthly team meetings to maintain consistency


### Disagreement Resolution Protocol

#### Step 1: Individual Review
- Annotator reviews their work against guidelines
- Check for obvious errors or oversights

#### Step 2: Peer Discussion
- Annotators discuss disagreement cases
- Reference guidelines and examples
- Attempt to reach consensus

#### Step 3: Senior Reviewer Decision
- If no consensus, team member with business background makes final decision
- Decision becomes reference for similar future cases
- Update guidelines if needed

#### Step 4: Documentation
- Record all disagreement cases and resolutions
- Track common disagreement patterns
- Update training materials
---

## 📊 Data Validation Checklist

Before submitting annotations, verify:

### Completeness Check
- [ ] All required fields filled
- [ ] No missing or blank entries
- [ ] Consistent formatting across entries

### Quality Check
- [ ] Product name matches category selection
- [ ] Selling points are specific and relevant
- [ ] Caption includes all required elements

### Consistency Check
- [ ] Similar products have similar selling points
- [ ] Category classifications are consistent
- [ ] Caption style matches guidelines

### Final Review
- [ ] Spell-check all text entries
- [ ] Confirm logical consistency across fields

---

## 📝 Annotation Tools and Templates

### Recommended Annotation Sheet Structure
```
| Image_ID | Product_Name | Category | Selling_Points | Caption |
```

*These guidelines ensure high-quality, consistent annotations that support reliable VLM evaluation and meaningful research conclusions. Regular adherence to these protocols is essential for maintaining the 90% inter-annotator agreement target.*