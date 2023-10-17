import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import altair as alt

# To not display warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

# Personalized side bar
st.sidebar.text("Marin VIGOT")
image_url = "south_african_blue_bird.jpg"
st.sidebar.image(image_url, use_column_width=True)
st.sidebar.text("This is my Streamlit website with a \n bird that I saw in South Africa.")

# links
github_link = "[My GitHub Profile](https://github.com/Mar1-hub)"
st.sidebar.markdown(github_link, unsafe_allow_html=True)
linkedin_link = "[My Linkedin Profile](https://www.linkedin.com/in/marin-vigot)"
st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
professor_link = "[My Professor Profile](https://www.linkedin.com/in/manomathew)"
st.sidebar.markdown(professor_link, unsafe_allow_html=True)


#title
st.markdown("<h1 style='text-align: center;'>Agriculture Impact on Environment</h1>", unsafe_allow_html=True)
    
# Create a space between the title and the other content
st.write("")  

# check box to put a new dataset
#new_dataset_option = st.checkbox("Check this case to upload a new dataset")


# Option for users to upload a new dataset

#if new_dataset_option:
#    uploaded_file = st.file_uploader("click on browse file to import your file.", type=["csv"])

#   if uploaded_file is not None:
#        df = load_data(uploaded_file)
#else:
    # Automatically load the default dataset 
#    default_file_path = "/home/myenv/uploaded_file.csv"
#    df = load_data(default_file_path)






#load the data
@st.cache_data
def load_data(nrows):
    df = pd.read_csv('Agribalyse_Synthese.csv')
    
    # delete code agb, code ciqual and code saison/avion because code saison/avion have only one value and AGB and ciqual don't have importance. 
    df.drop(columns=['Code AGB', 'Code CIQUAL', 'LCI Name'], inplace=True)
    
    # delete rows with dqr > 3 because dqr is a ratio to know if the data is ok. if it's near 5 it's bad , whereas near to 1 it's good.
    df = df[df['DQR'] <= 3]
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    return df



# print 10000 lines when show the data is check
df = load_data(10000)
'''Before using my dataframe, I cleaned it a little bit : I only take the lines with "dqr" attribute under 3 because it\'s the data quality ratio. If it\'s near 1 it\'s good and near five, bad.\n 
I also delete the code "AGB" and "CIQUAL" columns because those code doesn\'t mean anything for us, it\'s just to classify products. \n 
I finally delete the columns with "english products names" because the other variables are in french and we already have the "french products names"'''
if st.checkbox('Button to show the dataframe df'):
    st.subheader('Agribalyse data')
    st.write(df)




# PART I#######
#######
###
if st.button("Presentation of the data"):
### Correlation matrix
    # Select only integer and float columns for correlation
    numerical_columns = df.select_dtypes(include=['int64', 'float64'])
    '''
    -code agb: Agribalyse code \n
    -code ciqual: CIQUAL code  \n
    -groupe d'aliment: Food group to which the food belongs. E.g., infant food, various ingredients, beverages\n
    -sous-groupe d'aliment: Subgroup to which it belongs. E.g., herbs, seaweed, sauces, non-alcoholic beverages\n
    -nom du produit en français: Name given in France \n
    -lci name: LCI database name \n
    -code saison: Season number \n
    -code avion: Whether shipped by airplane or not \n
    -livraison: Temperature during delivery \n
    -matériau d'emballage: Type of packaging material \n
    -préparation: Whether preparation is required or not \n
    -dqr: Data quality ratio: Indicates the level of confidence in the score. - Close to 1: reliable; - Close to 5: significant uncertainty. Data with a DQR >= 3 is considered unreliable. \n
    -score unique ef: Eco-indicator in mPt (millipoint) per kg of product. 1 Pt corresponds to the annual environmental impact of one person. \n
    -changement climatique: Climate change impact in kg CO2/kg of product
    -appauvrissement de la couche d'ozone: Impact on ozone layer depletion in kg of trichlorofluoromethane: kg CFC-11/kg of product \n
    -rayonnements ionisants: Ionizing radiation by uranium in kg of U-235/kg of product
    -formation photochimique d'ozone: Impact on ground-level ozone presence (chemically harmful to health) in kg non-methane volatile organic compounds (kg NMVOC)/kg of product \n
    -particules fines: Impact on human health in disease incidence \n
    -effets toxicologiques sur la santé humaine substances non-cancérogènes: Impact on health from exposure to chemical contaminants in the environment (air, water, soil). E.g., pesticides, heavy metals, industrial pollutants. Exposure through direct ingestion of food containing pesticide residues is not currently integrated. In CTUh (Chronic Toxicity Units per hour). \n
    -effets toxicologiques sur la santé humaine: substances cancérogènes: Impact on health from exposure to chemical contaminants in the environment (air, water, soil). E.g., pesticides, heavy metals, industrial pollutants. Exposure through direct ingestion of food containing pesticide residues is not currently integrated. In CTUh (Chronic Toxicity Units per hour). \n
    -acidification terrestre et eaux douces: Chemical emissions into the atmosphere of acid in mol H+/kg of product \n
    -eutrophisation eaux douces: Enrichment in nutrients in kg of P/kg of product \n
    -eutrophisation marine: Same as eutrophication of freshwater, but in kg N/kg of product \n
    -eutrophisation terrestre: Same as eutrophication of freshwater, but in mol N/kg of product \n
    -ecotoxicité pour écosystèmes aquatiques d'eau douce: Contamination of freshwater ecosystems in CTUe \n
    -utilisation du sol: Impact on land degradation in points \n
    -épuisement des ressources eau: Impact on water withdrawal in m³ of water used related to local water scarcity. \n
    -épuisement des ressources énergétiques: Depletion of non-renewable energy resources in MJ \n
    -épuisement des ressources minéraux: kg of antimony (kg Sb)/kg of product recommended values. \n
     '''
    # Calculate the correlation matrix for numerical attributes
    corr_matrix = numerical_columns.corr()

    # Display the correlation matrix
    st.subheader("Correlation Matrix (Numeric Attributes Only):")
    st.write(corr_matrix)

    # Create a heatmap of the correlation matrix
    st.subheader("Correlation Heatmap (Numeric Attributes Only):")
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    st.pyplot()

    # Counter for the different groups 
    food_group_counts = df['groupe d\'aliment'].value_counts()
    
### pie plot distribution "groupe d'aliment"
    
    # pie chart dataframe
    groupe_aliment_counts = pd.DataFrame({'Groupe d\'aliment': food_group_counts.index, 'Count': food_group_counts})

    # interactive pie 
    fig = px.pie(groupe_aliment_counts, names='Groupe d\'aliment', values='Count',
             title=' "Groupes d\'Aliments" distribution')

  
    fig.update_traces(textinfo='percent+label', pull=0.05, hole=0.3)

    st.plotly_chart(fig)
    '''
    As you can see this is the distribution of food groups, you can check and uncheck the box on the right to display the groupe that you want
    '''

### Bar plot distribution "sous-groupe"

    # sub-food groups
    sous_groupe_counts = df['sous-groupe d\'aliment'].value_counts().reset_index()
    sous_groupe_counts.columns = ['Sous-Groupe d\'Aliment', 'Count']

    #interactive horizontal bar plot
    fig = px.bar(sous_groupe_counts, x='Count', y='Sous-Groupe d\'Aliment',
                 title='"Sous-Groupes d\'aliment" distribution',
                 labels={'Sous-Groupe d\'Aliment': 'Sous-Groupe d\'Aliment', 'Count': 'Count'},
                 color='Sous-Groupe d\'Aliment')
    
    fig.update_xaxes(categoryorder='total ascending')
    fig.update_layout(xaxis_title='Count', yaxis_title='Sous-Groupe d\'Aliment')
    fig.update_layout(height=600, width=800)  
    
    st.plotly_chart(fig)
        

### pie plot distribution "livraison"

    # values "livraison" counter 
    livraison_counts = df['livraison'].value_counts().reset_index()
    livraison_counts.columns = ['Livraison', 'Count']

    #  interactive pie plot
    fig = px.pie(livraison_counts, names='Livraison', values='Count',
                 title='"Livraison" distribution',
                 labels={'Livraison': 'Méthode de Livraison', 'Count': 'Nombre de Commandes'})

    st.plotly_chart(fig)

    ' the difference between "congelé" et "glacé" is the temperature : glacé -> between -18 and -24 degrees and congelé between -6 and -18 degrees. We can see that for better conservation of products, around half of them are delivered glacé.'
    
### pie plot distribution "matériau d'emballage"   

    # values "matériau d'emballage" counter
    emballage_counts = df['matériau d\'emballage'].value_counts().reset_index()
    emballage_counts.columns = ['Matériau d\'Emballage', 'Count']

    # interactive pie chart 
    fig = px.pie(emballage_counts, names='Matériau d\'Emballage', values='Count',
                 title='"Matériau d\'Emballage" distribution',
                 labels={'Matériau d\'Emballage': 'Matériau d\'Emballage', 'Count': 'Nombre d\'Occurences'})

    st.plotly_chart(fig)
    ' here we can see that lpde : kind of plastic made with "polystirene" that resist to cold temperature , PS : polystirène and PP: another plastique are the three materials more used. \n We can also see that carboard "carton",and as we saw in recent years there is a trend to replace plastic by cardboard'  
    
    
### pie plot distribution "préparation"  

    # values of "préparation" counter
    preparation_counts = df['préparation'].value_counts().reset_index()
    preparation_counts.columns = ['Préparation', 'Count']

    # interactive pie plot
    fig = px.pie(preparation_counts, names='Préparation', values='Count',
                 title='"Préparation" distribution',
                 labels={'Préparation': 'Préparation', 'Count': 'Nombre d\'Occurences'})

    st.plotly_chart(fig)

    ' Around 2 products out of 3 don\'t need any preparation'
    
### histogram score ef
    score_unique_ef = df['score unique ef']

    fig = px.histogram(score_unique_ef, nbins=20, title="Interactive Histogram of Score Unique EF")
    fig.update_layout(xaxis_title="Score Unique EF (mPt/kg of prod)", yaxis_title="Frequency")
    st.plotly_chart(fig)
    
    'The ef-score is a score that estimate the global écological impact of a product. The scale is in millipoint by kg of product. One point is equal to the environnemental impact of one person in a year.'
    
###
#######
#####################


# PART II #######
#######
###
# Create buttons to access different sections
if st.button("Health and Environnement impacts"):
    print("bienvenu")
    st.markdown("<h1 style='text-align: center;'> The purpose of the analysis of this dataframe is to know wich group of aliments and aliments are the best ad worst for the environnement health \n \n </h1>", unsafe_allow_html=True)
### 10 "groupe d'aliment" values with the higher changement clim value"    
        #title
    st.markdown("<h1 style='text-align: center;'> Climate change </h1>", unsafe_allow_html=True)
    top_10_groupe_aliment = df.nlargest(10, 'changement climatique')

    # interactive pie plot
    fig = px.pie(top_10_groupe_aliment, names='groupe d\'aliment', values='changement climatique',
                 title='10 "groupe d\'aliment" values with the biggest impact on climate change',
                 labels={'groupe d\'aliment': 'Groupe d\'Aliment', 'changement climatique': 'Changement Climatique'})

    st.plotly_chart(fig)
    
    
    # number of rows with "groupe d'aliment" = "viandes,oeufs poissons"

    count_viandes_oeufs_poissons = df[df['groupe d\'aliment'] == 'viandes, œufs, poissons'].shape[0]

    # Print the result
    st.write(f"Number of rows with 'groupe d'aliment' equal to 'viandes, oeufs, poissons': {count_viandes_oeufs_poissons}")
    '''above I calculate the number of rows corresponding to oeuf,vaindes,poisson'''
    '''    \n The unit of our values is kg of CO2 emission by kg of product. That means that only with the data in our df, there is a half     tonne of CO2 emission for 403 kilos of product so CO2 emission created represent around 125% of product created '''
    

### "changement climatique" 
    
    # mean "changement climatique" value for each "groupe d'aliment" 
    mean_changement_climatique = df.groupby('groupe d\'aliment')['changement climatique'].mean().reset_index()

    # interactive pie plot
    fig = px.pie(mean_changement_climatique, names='groupe d\'aliment', values='changement climatique',
                 title='Mean climate change by "Groupe d\'Aliment"',
                 labels={'groupe d\'aliment': 'Groupe d\'Aliment', 'changement climatique': 'Moyenne du Changement Climatique'})

    st.plotly_chart(fig)
    
    ''' Here we don't have 100% 'viandes,poissons,oeuf' because we calculate the mean and because this group was the most represented in           the dataframe, we had 100% in the top 10 when we didn't calculate the mean.
    \n Here we can see that 30% of CO2 emission is linked to animal products. That's why a lot of people become vegan for environnement         convictions.
    '''
      
    #  mean "changement climatique" value for each "sous-groupe d'aliment"
    mean_changement_climatique_by_sous_groupe = df.groupby('sous-groupe d\'aliment')['changement climatique'].mean().reset_index()

    # top 20 highest mean values
    top_20_mean_changement_climatique = mean_changement_climatique_by_sous_groupe.nlargest(20, 'changement climatique')

    fig = px.pie(top_20_mean_changement_climatique, names='sous-groupe d\'aliment', values='changement climatique',
                 title='Top 20 "Sous-Groupe d\'Aliment"with biggest mean of "Changement Climatique"',
                 labels={'sous-groupe d\'aliment': 'Sous-Groupe d\'Aliment', 'changement climatique': 'Moyenne du Changement Climatique'})
    
    st.plotly_chart(fig)
    'we did the same for the variable "sous-groupe d\'aliment". We have more precision on what products are the badest for the climate change. As we can see the 2 most important values of CO2 emission are cooked product. It is very logical because you add to the emission of the product in itself, the emission of its preparation. That is why those product are the most bad .'  

    
    # top 10 lowest mean values
    
    top_10_lowest_mean_changement_climatique = mean_changement_climatique_by_sous_groupe.nsmallest(10, 'changement climatique')
    #  pie plot 
    fig = px.pie(top_10_lowest_mean_changement_climatique, names='sous-groupe d\'aliment', values='changement climatique',
                 title='Top 10 "Sous-Groupe d\'Aliment" with lowest mean of "Changement Climatique"',
                 labels={'sous-groupe d\'aliment': 'Sous-Groupe d\'Aliment', 'changement climatique': 'Moyenne du Changement Climatique'})

    st.plotly_chart(fig)

    'we did the same for the 10 "sous-groupe" with the lowest values and obviously, water is the lowest value because this is the less transformed product.Near we have condiments like salt, sugar and "aide culinaire", for the same reason'
    
# Top 100 Products with Highest Mean "changement climatique"
    mean_changement_climatique_by_product = df.groupby('nom du produit en français')['changement climatique'].mean().reset_index()
    top_100_products = mean_changement_climatique_by_product.nlargest(100, 'changement climatique')

    fig = px.bar(top_100_products, x='nom du produit en français', y='changement climatique',
                 title='Top 100 Products with highest Changement Climatique mean',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'changement climatique': 'Moyenne du Changement Climatique'})
    fig.update_xaxes(categoryorder='total descending')
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)
    'To go further, I decided to see precisely the 100 products with the biggest impact. The top 4 is only cooked lamb. That is because lamb needs to be cooked more time than other meat and that is creating more CO2. Top 5 you have cooked beef and then raw lamb and beef. If you click on all the bars separately, you will see that the top 100 is only  constituted of meat.'
    
    # Top 20 Products with Lowest Mean "changement climatique"
    top_20_lowest_products = mean_changement_climatique_by_product.nsmallest(20, 'changement climatique')

    fig = px.bar(top_20_lowest_products, x='nom du produit en français', y='changement climatique',
                 title='Top 20 Produits with lowest "Changement Climatique" mean',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'changement climatique': 'Moyenne du Changement Climatique'})
    fig.update_xaxes(categoryorder='total descending')
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig) 
    
    'After I did that with lowest value for "products". Here we have only products that can be consumated as a drink, with tea in last position. So when we have a class break, don\'t hesitate to take a tea !'

### Appauvrissement couche d'ozone
    st.markdown("<h1 style='text-align: center;'> Appauvrissement couche d\'ozone </h1>", unsafe_allow_html=True)

    # Mean Value by "groupe d'aliment"
    average_appauvrissement = df.groupby('groupe d\'aliment')['appauvrissement de la couche d\'ozone'].mean().reset_index()

    # Sort by the average value in ascending order
    average_appauvrissement_sorted = average_appauvrissement.sort_values(by='appauvrissement de la couche d\'ozone', ascending=True)

    fig = px.bar(average_appauvrissement_sorted, x='groupe d\'aliment', y='appauvrissement de la couche d\'ozone',
                 title='Mean of "Appauvrissement de la Couche d\'Ozone" by "Groupe d\'Aliment" (Ordre Croissant)',
                 labels={'groupe d\'aliment': "Groupe d'Aliment", 'appauvrissement de la couche d\'ozone': "Moyenne de l'Appauvrissement de la Couche d'Ozone"})
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)
    
    'For the group of products with highest mean value for "appauvrissement couche d\'ozone, we don\'t find meat first but vegetables. That is because the agriculture have a direct impact on ozone because of pesticid and other bad products that are directly going in the air.'
    
    # Top 30 Products with Highest Mean "Appauvrissement couche d'ozone"
    mean_appauvrissement_couche_ozone_by_product = df.groupby('nom du produit en français')['appauvrissement de la couche d\'ozone'].mean().reset_index()
    top_30_products = mean_appauvrissement_couche_ozone_by_product.nlargest(30, 'appauvrissement de la couche d\'ozone')

    fig = px.bar(top_30_products,x='nom du produit en français', y='appauvrissement de la couche d\'ozone',
                 title='Top 30 Products by "Appauvrissement de la Couche d\'Ozone" mean',
                 labels={'appauvrissement de la couche d\'ozone': "Moyenne de l'Appauvrissement de la Couche d'Ozone", 'nom du produit en français': 'Nom du Produit en Français'},)
    fig.update_yaxes(categoryorder='total descending')
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

    ' When we see the products, "datte" is first and has a very high value comparing to the other products. It can be a problem of input values in the dataframe or it can be because "datte" is very dry and because it is very exported: since 2019 the exportation was 23% higher than before and the impact of plane to ozone is very high. It can also because date fruit is produced in north africa and because africa is poor comparing to other continents, the farmers cannot use good products that do not have negative impact because it is more expensive'  
    
    # Top 30 Products with Lowest Mean "appauvrissement couche d'ozone"
    top_30_lowest_products = mean_appauvrissement_couche_ozone_by_product.nsmallest(30, 'appauvrissement de la couche d\'ozone')

    fig = px.bar(top_30_lowest_products, x='nom du produit en français', y='appauvrissement de la couche d\'ozone',
                 title="Top 30 Products with lowest  'Appauvrissement de la Couche d'Ozone' mean",
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'appauvrissement de la couche d\'ozone': "Moyenne de l'Appauvrissement de la Couche d'Ozone"},
                 color='nom du produit en français')  
    fig.update_xaxes(categoryorder='total descending')
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)
    ' For the products with the lowest values, we find again a lot of drinkable products and also sweet potatoes. It can be one of the best vegetables.'
    
    
### "Rayonnement ionisant" 
    st.markdown("<h1 style='text-align: center;'> Rayonnement ionisant </h1>", unsafe_allow_html=True)
    mean_rayonnements_ionisants_by_group = df.groupby('groupe d\'aliment')['rayonnements ionisants'].mean().reset_index()

    fig = px.bar(mean_rayonnements_ionisants_by_group, x='groupe d\'aliment', y='rayonnements ionisants',
                 title='Mean Rayonnements Ionisants by Groupe d\'Aliment',
                 labels={'groupe d\'aliment': "Groupe d'Aliment", 'rayonnements ionisants': 'Mean Rayonnements Ionisants'},
                 color='groupe d\'aliment')  # Add color to the bars
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

    ' For "rayonnement iosnisant" (that correspond to the kg of radiation of uranium by kg of a product creation),we don\'t find the same group ranking than the previous ones. Condiments are first, then meat and the third rank goes to prepared starters. The health impact of those products when they are created is bad comparing to ther products. For condiments and prepared starters,it is certainly because they need some industrial transformation and the use of machine create uranium emission.'
    
    # Top 30 Products with Highest Mean 'rayonnements ionisants'
    top_30_highest_products = df.groupby('nom du produit en français')['rayonnements ionisants'].mean().nlargest(30)

    fig = px.bar(top_30_highest_products.reset_index(), x='nom du produit en français', y='rayonnements ionisants',
                 title='30 product with highest mean of "Rayonnements Ionisants"',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'rayonnements ionisants': 'Moyenne des Rayonnements Ionisants'},
                 color='rayonnements ionisants', color_continuous_scale='Bluered')

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)
    'For the top 30 products with higher values, we have dry products first because you need to dry them with industrial mechanism.'

    # Top 30 Products with Lowest Mean 'rayonnements ionisants'
    top_30_lowest_products = df.groupby('nom du produit en français')['rayonnements ionisants'].mean().nsmallest(30)

    fig = px.bar(top_30_lowest_products.reset_index(), x='nom du produit en français', y='rayonnements ionisants',
                 title='30 product with lowest mean "Rayonnements Ionisants"',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'rayonnements ionisants': 'Moyenne des Rayonnements Ionisants'},
                 color='rayonnements ionisants', color_continuous_scale='Bluered')

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

    'The top 30 lowest is composed in majority by untransformed products'
        
### formation photochimique d'ozone

    st.markdown("<h1 style='text-align: center;'> Formation photochimique d'ozone </h1>", unsafe_allow_html=True)
    'The results of "formation photochimique d\'ozone are very near the results of "appauvrissement couche d\'ozone, I will not comment them'
    # Mean de 'formation photochimique d'ozone' by groupe d'aliment
    mean_formation_photochimique_by_group = df.groupby('groupe d\'aliment')['formation photochimique d\'ozone'].mean().reset_index()

    fig = px.bar(mean_formation_photochimique_by_group, x='groupe d\'aliment', y='formation photochimique d\'ozone',
                 title='Mean of "Formation Photochimique d\'Ozone" by "Groupe d\'Aliment" ',
                 labels={'groupe d\'aliment': 'Groupe d\'Aliment', 'formation photochimique d\'ozone': 'Moyenne de Formation Photochimique d\'Ozone'},
                 color='formation photochimique d\'ozone')

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    fig.update_xaxes(categoryorder='total ascending')  # Tri par ordre croissant
    st.plotly_chart(fig)


    # Top 30 Products with Highest Mean 'formation photochimique d'ozone'
    top_30_highest_products = df.groupby('nom du produit en français')['formation photochimique d\'ozone'].mean().nlargest(30)

    fig = px.bar(top_30_highest_products.reset_index(), x='nom du produit en français', y='formation photochimique d\'ozone',
                 title='Top 30 products with highest "Formation Photochimique d\'Ozone" value',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'formation photochimique d\'ozone': 'Moyenne de Formation Photochimique d\'Ozone'},
                 color='formation photochimique d\'ozone', color_continuous_scale='Bluered')

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

    # Top 30 Products with Lowest Mean 'formation photochimique d'ozone'
    top_30_lowest_products = df.groupby('nom du produit en français')['formation photochimique d\'ozone'].mean().nsmallest(30)

    fig = px.bar(top_30_lowest_products.reset_index(), x='nom du produit en français', y='formation photochimique d\'ozone',
                 title='Top 30 products with lowest "Formation Photochimique d\'Ozone" value',
                 labels={'nom du produit en français': 'Nom du Produit en Français', 'formation photochimique d\'ozone': 'Moyenne de Formation Photochimique d\'Ozone'},
                 color='formation photochimique d\'ozone', color_continuous_scale='Bluered')

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

### particules fines
    st.markdown("<h1 style='text-align: center;'> Particules fines </h1>", unsafe_allow_html=True)
    'This attributes is very linked with human health. Fine particles are particles wich are in the air and wich can create cardiac and pulmonary problems. The unit is an incidence value on human health' 
    
    # mean de 'particules fines' by groupe d'aliment
    mean_particules_fines_by_group = df.groupby('groupe d\'aliment')['particules fines'].mean().reset_index()

    # top 30 most important value
    top_30_highest_products = df.nlargest(30, 'particules fines')[['nom du produit en français', 'particules fines']]
    
    # Top 30 less important value
    top_30_lowest_products = df.nsmallest(30, 'particules fines')[['nom du produit en français', 'particules fines']]


    fig1 = px.bar(mean_particules_fines_by_group, x='groupe d\'aliment', y='particules fines',
                  title='Mean "Particules Fines" by "Groupe d\'Aliment"',
                  labels={'groupe d\'aliment': 'Groupe d\'Aliment', 'particules fines': 'Moyenne de Particules Fines'},
                  color='particules fines')
    fig1.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig1.update_layout(clickmode='event+select')
    fig2 = px.bar(top_30_highest_products, x='nom du produit en français', y='particules fines',
                  title='Top 30 products with highest "Particules fines" value',
                  labels={'nom du produit en français': 'Nom du Produit en Français', 'particules fines': 'Particules Fines'},
                  color='particules fines')
    fig2.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig2.update_layout(clickmode='event+select')

    fig3 = px.bar(top_30_lowest_products, x='nom du produit en français', y='particules fines',
                  title='Top 30 products with lowest "Particules fines" value',
                  labels={'nom du produit en français': 'Nom du Produit en Français', 'particules fines': 'Particules Fines'},
                  color='particules fines')
    fig3.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig3.update_layout(clickmode='event+select')


    st.plotly_chart(fig1)
    'We can observe that products linked to animals like meat, eggs, fish or milk have the highest values. There are also transformed meal like prepared starters that are very high. The mean value of those products is not alarming but if you multiply that by each creation of products, that is very big'
    
    st.plotly_chart(fig2)
    ' The top highest values are for 70% of them lamb meat . We can consider that lamb is certainly the worst meat to produce'
    st.plotly_chart(fig3)
    'water and drinkable ressources are another time the lowest important values'
    
### 'acidification terrestre et eaux douces'
    st.markdown("<h1 style='text-align: center;'> Acidification terrestres et eaux douces</h1>", unsafe_allow_html=True)
    ' The acidification of ground and water is showing the amount of H+ (hydrogen ion) adding to the ground and water. This quantity is altering the acid aspect of them and can create the extinction of some species that cannot adapt to this acidification.'
    '\n The results are the same that for fine particles, I will not comment them'

    # mean by food group
    mean_acidification_terrestre_by_group = df.groupby('groupe d\'aliment')['acidification terrestre et eaux douces'].mean().reset_index()

    # Top 30 French products with the highest values
    top_30_highest_products = df.nlargest(30, 'acidification terrestre et eaux douces')[['nom du produit en français', 'acidification terrestre et eaux douces']]

    # Top 30 French products with the lowest values
    top_30_lowest_products = df.nsmallest(30, 'acidification terrestre et eaux douces')[['nom du produit en français', 'acidification terrestre et eaux douces']]
    
    fig1 = px.bar(mean_acidification_terrestre_by_group, x='groupe d\'aliment', y='acidification terrestre et eaux douces',
                  title='Mean "acidification terrestre et eaux douces" by "groupe d\'aliment"',
                  labels={'groupe d\'aliment': 'Food Group', 'acidification terrestre et eaux douces': 'moyenne par groupe'},
                  color='acidification terrestre et eaux douces', color_continuous_scale='Blues')


    fig1.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig1.update_layout(clickmode='event+select')


    st.plotly_chart(fig1)

    # top_30_highest_products 
    fig2 = px.bar(top_30_highest_products, x='nom du produit en français', y='acidification terrestre et eaux douces',
                  title='Top 30 products with highest "acidification terrestre et eaux douces" value',
                  labels={'nom du produit en français': 'Product Name (in French)', 'acidification terrestre et eaux douces': 'Acidification Terrestre et Eaux Douces'},
                  color='acidification terrestre et eaux douces', color_continuous_scale='Reds')


    fig2.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig2.update_layout(clickmode='event+select')

    st.plotly_chart(fig2)

    # Top 30 lowest products 
    fig3 = px.bar(top_30_lowest_products, x='nom du produit en français', y='acidification terrestre et eaux douces',
                  title='Top 30 products with lowest "acidification terrestre et eaux douces" value',
                  labels={'nom du produit en français': 'Product Name (in French)', 'acidification terrestre et eaux douces': 'Acidification Terrestre et Eaux Douces'},
                  color='acidification terrestre et eaux douces', color_continuous_scale='Greens')


    fig3.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig3.update_layout(clickmode='event+select')

    st.plotly_chart(fig3)



### "Changement clim" by "code avion"
    st.markdown("<h1 style='text-align: center;'> Plane impact on climate change </h1>", unsafe_allow_html=True)
    
    changement_climatique = df['changement climatique']
    code_avion = df['code avion']

    fig, ax = plt.subplots()
    box_plot_data = [changement_climatique[code_avion == code] for code in code_avion.unique()]
    ax.boxplot(box_plot_data, labels=code_avion.unique())
    ax.set_title("Box Plot of Changement Climatique by Code Avion")
    ax.set_xlabel("Code Avion")
    ax.set_ylabel("Changement Climatique (kg CO2/kg de produit)")

    st.pyplot(fig)

    'The boxplots show that even if we have much values of 0 for code avion (products that are not transported by plane), the mean of CO2 emission by kg of products is higher when the value is 1 ( when a product is transported by plane). So the plane is one of the main cause of climate change'
    
    
###   "climate change" by "preparation" 
    st.markdown("<h1 style='text-align: center;'> climate change value by preparation </h1>", unsafe_allow_html=True)
    mean_changement_climatique = df.groupby('préparation')['changement climatique'].mean()


    st.bar_chart(mean_changement_climatique)
    'Finally, we can see that the way of preparation has an impact on CO2 emission. It is logical because when you cook something in a pan or in an oven, you create smoke that is composed of CO2 and that is directly rejected to the air. We can see that the best solutions are to cook in water your aliments when it is possible or to fries: there is less smoke when you fried something that when you cook something in a pan because the product is not in direct contact with a very hot metals but with the boiling oil. What causes smoke is the friction between hot metals and fresh product.'
    
### climate change by "matériau d'emballage"
   
    mean_changement_climatique = df.groupby('matériau d\'emballage')['changement climatique'].mean().reset_index()
    fig = px.pie(mean_changement_climatique, values='changement climatique', names='matériau d\'emballage', title='Interactive Pie Chart of Mean Changement Climatique by Matériau d\'Emballage')
    st.plotly_chart(fig)
    
    'We see that plastic is the badest materials used in our industries. We also see that it is the most used materials. The carton linked to plastic is in the top 3 badest but alone it is better so we can make a transition from plastic to carton.'
    
###
#######
#####################


    
# PART 3 #######
#######
###
if st.button("Conclusion"):
    '''
    About the results, what we can recommend and what we need to reduce for good health and environnement :
    - Less meat, specificly lamb : We have seen that meat has been in the top 2 group of products with all the environnemental and health attributes mean value. \n
    - In general, you need to reduce all the products linked to animal husbandry(élevage) \n
    - But I don't know if it's good to completly stop those products because we don't really know if becoming vegan can bring all the nutriments that we need to be in good health. \n
    -Reduce or completely stop transformed products and try to make yourself all your meal with fresh and untransformed product. \n
    - Use less plastic and plane for the transport of products. We need to try to buy more local and we can also buy directly our products to a farmer to reduce more and more the transport impact that is very big. \n
    
    About the way that I present the dataframe:
    - I have chose to concentrate my analysis on group of products and product that have the most/less important impact. Because of that I have a lot of time the same type of diagram. \n
    -I chose barplot and pieplot because I have tested other plot that were very ugly to see. I think to see distribution, pieplot and barplot are the best graphics. \n
    -I encountered some problems with two attributes : "effets toxicologiques sur la santé humaine substances non-cancérogènes" and effets toxicologiques sur la santé humaine substances cancérogènes" because there was a syntax error an streamlit didn't want to find them . \n
    - Last but not least, it would have been interesting to have attributes about time and locations to create maps and see the evolution over time
    '''
###
#######
#####################    
    
    
