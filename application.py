# Core Pkg
import streamlit as st 
import streamlit.components.v1 as stc 


# Load EDA
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


# Load Our Dataset
def load_data(data):
    df = pd.read_csv(data)
    return df 


# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(data):
    count_vect = CountVectorizer()
    cv_mat = count_vect.fit_transform(data)
    # Get the cosine
    cosine_sim_mat = cosine_similarity(cv_mat)
    return cosine_sim_mat



# Recommendation Sys
@st.cache
def get_recommendation(content,cosine_sim_mat,df,num_of_rec=10):
    # indices of the course
    rec_indices = pd.Series(df.index,index=df['content']).drop_duplicates()
    # Index of course
    idx = rec_indices[content]

    # Look into the cosine matr for that index
    sim_scores =list(enumerate(cosine_sim_mat[idx]))
    sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)
    selected_indices = [i[0] for i in sim_scores[1:]]
    selected_scores = [i[0] for i in sim_scores[1:]]

    # Get the dataframe & title
    result_df = df.iloc[selected_indices]
    result_df['similarity_score'] = selected_scores
    final_recommended = result_df[['id','similarity_score','listing_url','price','description','property_type']]
    return final_recommended_.head(num_of_rec)



# Search For Course 
@st.cache
def search_term_if_not_found(term,df):
    result_df = df[df['content'].str.contains(term)]
    return result_df


def main():

    st.title("Boston Airbnb Recommendation App")

    menu = ["Home","Recommend","EDA & Data Visulizations"]
    choice = st.sidebar.selectbox("Menu",menu)

    df = load_data(r"content_out.csv")

    if choice == "Home":
        st.subheader("Home")
        st.dataframe(df.head(10))


    elif choice == "Recommend":
        st.subheader("Recommend Listings:")
        cosine_sim_mat = vectorize_text_to_cosine_mat(df['content'])
        search_term = st.text_input("Search")
        num_of_rec = st.sidebar.number_input("Number",4,30,7)
        if st.button("Recommend"):
            if search_term is not None:
                try:
                    results = get_recommendation(search_term,cosine_sim_mat,df,num_of_rec)
                    with st.beta_expander("Results as JSON"):
                        results_json = results.to_dict('index')
                        st.write(results_json)

                    for row in results.iterrows():
                        rec_title = row[1][0]
                        rec_score = row[1][1]
                        rec_url = row[1][2]
                        rec_price = row[1][3]
                        rec_num_sub = row[1][4]

                        # st.write("Title",rec_title,)
                        stc.html(RESULT_TEMP.format(rec_title,rec_score,rec_url,rec_url,rec_num_sub),height=350)
                except:
                    results= "Not Found"
                    st.warning(results)
                    st.info("Suggested Options include")
                    result_df = search_term_if_not_found(search_term,df)
                    st.dataframe(result_df)


                # How To Maximize Your Profits Options Trading




    else:
        st.subheader("EDA & Data Visulizations")
        st.text("Built with Streamlit & Pandas")
        html_temp = """<div class='tableauPlaceholder' id='viz1639794308819' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='BostonAirbnbAnalysis_16397915993500&#47;Dashboard3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1639794308819');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.90)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='9000px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        stc.html(html_temp, width=900,height=1200)

        html_temp2 = """<div class='tableauPlaceholder' id='viz1639795658312' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='BostonAirbnbAnalysis2&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1639795658312');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        stc.html(html_temp2, width=900,height=1000)

        html_temp3 = """<div class='tableauPlaceholder' id='viz1639795755158' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='BostonAirbnbAnalysis3&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1639795755158');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='927px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        stc.html(html_temp3, width=900,height=1000)


if __name__ == '__main__':
    main()
