import os

PROJECT_REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(PROJECT_REPORT_DIR, "final_mca_project_report.md")

# Chronological order of chapters to combine
CHAPTER_FILES = [
    "chapter_1_title_page.md",
    "chapter_2_certificate.md",
    "chapter_3_declaration.md",
    "chapter_4_acknowledgement.md",
    "chapter_5_abstract.md",
    "chapter_6_toc.md",
    "chapter_7_introduction.md",
    "chapter_8_problem_statement.md",
    "chapter_9_objectives.md",
    "chapter_10_scope.md",
    "chapter_11_literature_review.md",
    "chapter_12_srs.md",
    "chapter_13_system_analysis.md",
    "chapter_14_feasibility_study.md",
    "chapter_15_sdlc.md",
    "chapter_16_system_design.md",
    "chapter_17_database_design.md",
    "chapter_18_implementation.md",
    "chapter_19_nlp_methodology.md",
    "chapter_20_testing.md",
    "chapter_21_results.md",
    "chapter_22_applications.md",
    "chapter_23_advantages.md",
    "chapter_24_limitations.md",
    "chapter_25_future_scope.md",
    "chapter_26_conclusion.md",
    "chapter_27_references.md"
]

def compile_report():
    print(f"Compiling final project report into {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for idx, filename in enumerate(CHAPTER_FILES):
            filepath = os.path.join(PROJECT_REPORT_DIR, filename)
            
            if not os.path.exists(filepath):
                print(f"[ERROR] Chapter file missing: {filepath}")
                continue
                
            print(f"  Appending {filename}...")
            with open(filepath, "r", encoding="utf-8") as infile:
                content = infile.read().strip()
                
                # Write content
                outfile.write(content)
                
                # Append page break if not the last chapter
                if idx < len(CHAPTER_FILES) - 1:
                    outfile.write("\n\n---\n<!-- Page Break -->\n\\newpage\n\n")
                    
    print("Report compilation complete!")

if __name__ == "__main__":
    compile_report()
