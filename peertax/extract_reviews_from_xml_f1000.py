# Configuration
import os
import re
import pandas as pd
from lxml import etree
from tqdm import tqdm_notebook as tqdm
from peertax import xml

paper_folder = '../data/articles/f1000_articles/'

# Extract reviews
revs = []
for doc in tqdm(os.listdir(paper_folder)):
    if not doc.endswith('.xml'):
        continue
    fullname = os.path.join(paper_folder, doc)
    if os.stat(fullname).st_size != 0:
        tree = etree.parse(fullname)
        # Only select body of reviews
        children = tree.findall("//sub-article[@article-type='ref-report']/body")
        for i in children:
            revs.append(re.sub(r'\t+', '', xml.get_text_content(i)))

# Put reviews in a dataframe
df = pd.DataFrame({'Reviews': revs})

# Save the dataframe
df.to_csv('../data/reviews/f1000_reviews.csv')
