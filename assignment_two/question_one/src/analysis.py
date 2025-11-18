import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil
from PIL import Image
from fpdf import FPDF

# Read in the clean data using pandas
df = pd.read_csv('../data_clean/clean_yield_data.csv')

# Create temp folder to save images
temp_folder = "../temp"
path = os.path.join(temp_folder)
os.makedirs(temp_folder, exist_ok=True)

# Convert width and height from px to in because figsize accept inch only ( in=px/dpi )
width=800/300
height=600/300
# Prepare figure
plt.figure(figsize=(width,height), dpi=300)

# V1: Math score and reading score grouped by gender


    # Melt will put both math and reading score ontop of each other in new column called Subject and thier values will be in new column called Score ( convert data wide -> long)
df_melted = df.melt( 
    id_vars="gender", 
    value_vars=["math score", "reading score"], 
    var_name="Subject", 
    value_name="Score"
)

sns.boxplot(x="Subject", y="Score", hue="gender", data=df_melted)
plt.title("Math vs Reading Scores by Gender")
plt.xlabel("Subject")
plt.ylabel("Score")
plt.legend(title="Gender" ,fontsize='6',loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(temp_folder+"/V1.png", dpi=300,bbox_inches="tight")

plt.clf()
# V2: Math score by test preparation course
sns.barplot(x='test preparation course', y='math score', data=df, palette='pastel')
plt.title('Math Scores by Test Preparation Course')
plt.ylabel('Math Score')
plt.xlabel('Test Preparation Course')

plt.savefig(temp_folder+"/V2.png", dpi=300,bbox_inches="tight")


plt.clf()
# V3: Overall_avg mean of all the scores
lunch_subject_means = df.groupby("lunch")[["math score","reading score","writing score"]].mean().reset_index() # reset_index() converts the group labels (lunch) from index -> column because seaborn expect regular columns, not indexes.

lunch_melted = lunch_subject_means.melt(id_vars="lunch",
                                        value_vars=["math score","reading score","writing score"],
                                        var_name="Subject",
                                        value_name="Average Score")

    # Plot grouped bar chart
sns.barplot(x="lunch", y="Average Score", hue="Subject", data=lunch_melted, palette="muted")
plt.title("Average Subject Scores by Lunch Type")
plt.ylabel("Average Score")
plt.xlabel("Lunch Type")
plt.legend(title="Subject" ,fontsize='6',loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(temp_folder+"/V3.png", dpi=300,bbox_inches="tight")




plt.clf()
# V4: Correlation heatmap for math, reading and writing
corr = df[['math score','reading score','writing score']].corr()
sns.heatmap(corr, annot=True, vmin=-1, vmax=1)
plt.title('Correlation Between Subjects')

plt.savefig(temp_folder+"/V4.png", dpi=300,bbox_inches="tight")


plt.clf()
# V5: Math vs Reading with Trend Lines by Test Prep
sns.scatterplot(x='reading score', y='math score', hue='test preparation course', data=df)
sns.regplot(x='reading score', y='math score', data=df[df['test preparation course']=='completed'],
            scatter=False, label='Completed Fit', color='blue')
sns.regplot(x='reading score', y='math score', data=df[df['test preparation course']=='none'],
            scatter=False, label='None Fit', color='orange')
plt.title('Math vs Reading Scores by Test Preparation Course')
plt.xlabel('Reading Score')
plt.ylabel('Math Score')
plt.legend(title='Test Prep',fontsize='6',loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(temp_folder+"/V5.png", dpi=300,bbox_inches="tight")
plt.close()

# Reporting

figures = ["V1.png", "V2.png", "V3.png", "V4.png", "V5.png"]
titles = [
    "V1: Math vs Reading Scores by Gender",
    "V2: Math Scores by Test Preparation Course",
    "V3: Average Performance by Lunch Type",
    "V4: Correlation Between Subjects",
    "V5: Math vs Reading with Trend Lines by Test Prep"
]
interpretations = [
    '''
- The boxplots show that female students generally have higher reading scores than male students but male students have higher scores in math.
- Female student have a wider spread in math.
- Female student have more potential outliers.
- Male students performance are more consistent in both subjects than female score
- Overall, gender differences are more pronounced in reading than in math.
''',
    '''
- The bar plot show that students who completed test prep score have slightly higher scores in math.
- Completing test prep seems to improve math performance consistently.
''',
    '''
- The grouped bar show that lunch type has a noticeable impact on student outcomes.
- Students with standard lunch tend to have higher overall average scores.
- Students on free/reduced lunch have lower average performance.
- Standard lunch students appear to perform consistently across subjects.
''',
    '''
- Math, reading, and writing scores are positively correlated.
- Reading and writing have the strongest correlation.
- Math shows a moderate correlation with reading and writing.
''',
    '''
- Math and reading scores are positively associated for both groups.
- Students who completed test preparation have a slightly steeper trend line.
- Scatter points show that some students without test prep score very low in both subjects.
- Completion of the test prep course reduces extreme low scores.
'''
]

# Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for i, (fig, title, report) in enumerate(zip(figures, titles, interpretations)):
    pdf.add_page()
    
    # Main report title only on first page
    if i == 0:
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Students Performance Report", 0, 1, 'C')
        pdf.ln(5)

    # Figure caption
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, title, 0, 1, 'C')

    # Image
    img_path = os.path.join(temp_folder, fig)
    x = 15
    w = 180
    pdf.image(img_path, x=x, y=pdf.get_y(), w=w)
    
    # Compute image height in PDF units and move cursor below it
    
    with Image.open(img_path) as im:  # use with to auto-close
        img_width_px, img_height_px = im.size
        pdf_w_pt = 180  
        pdf_h_pt = img_height_px * pdf_w_pt / img_width_px
    pdf.set_y(pdf.get_y() + pdf_h_pt + 5) 

    # Interpretation text
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 7, report)

# Save PDF
pdf.output('../reports/report.pdf', 'F')

shutil.rmtree(temp_folder)  # delete temp folder