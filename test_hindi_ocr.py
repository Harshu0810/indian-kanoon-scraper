from hindiOCR import extract_hindi_paragraphs_from_pdf

PDF = r"C:\Users\Harsh\OneDrive\Desktop\hindi_judgment.pdf"

paras = extract_hindi_paragraphs_from_pdf(PDF)

print(len(paras))
print(paras[:2])
