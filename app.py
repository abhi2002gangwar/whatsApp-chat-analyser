import streamlit as st
import prepro
import support
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
st.sidebar.title("Analyse Your Chat")

uploaded_file = st.sidebar.file_uploader("Select a file to Analyze:")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # printing file name/chat name
    a = str(uploaded_file)[44:]
    b = a.split('.txt')
    # st.title('WhatsApp Chat Analysis with {}'.format(b[0]))
    # st.title()

    # View data on webpage
    # st.text(data)

    df = prepro.preprocess(data)

    # display DF on webpage
    # st.dataframe(df)

    # unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')

    if 'grp_notification' in user_list:
        user_list.remove('grp_notification')
        df = df[df['user'] != 'grp_notification']

    selected_user = st.sidebar.selectbox('Select User', user_list)

    if st.sidebar.button('Analyse'):

        # stats
        st.title('Chat Stats:')
        tot_msgs, tot_words, tot_media, tot_links = support.fetch_stats(
            df, selected_user)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.header(tot_msgs)

        with col2:
            st.header('Total words')
            st.header(tot_words)

        with col3:
            st.header('Shared media')
            st.header(tot_media)

        with col4:
            st.header('Shared Links')
            st.header(tot_links)

        # Timelines
        mtimeline, dtimeline = support.timeline(df, selected_user)
        busyday, busymonth = support.weeklyact(df, selected_user)

        col1, col2 = st.columns(2)

        with col1:
            st.title('Monthly Timeline:')
            fig, ax = plt.subplots()
            ax.plot(mtimeline['monyear'], mtimeline['message'], 'g-')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(busymonth.index, busymonth.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title('Daily Timeline:')
            fig, ax = plt.subplots()
            ax.plot(dtimeline['_date_'], dtimeline['message'], 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(busyday.index, busyday.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # busiest user in group chat
        if selected_user == 'Overall' and len(df['user'].unique()) > 2:

            st.title('Chattiest Users:')

            busyppl, dftable = support.busiest_ppl(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.pie(busyppl.values, labels=dftable['percentage'].head())
                plt.legend(busyppl.index, loc='center left')
                plt.axis('equal')
                st.pyplot(fig)

            with col2:
                st.dataframe(dftable, height=375, width=1500)

        # wordcloud
        st.title('Word Cloud:')
        dfwc = support.wrdcld(df, selected_user)
        fig, ax = plt.subplots()
        ax.imshow(dfwc)
        plt.axis('off')
        st.pyplot(fig)

        # Mostly used words
        st.title('Mostly Used Words:')

        col1, col2 = st.columns(2)

        popwords, dfwc = support.popwords(df, selected_user)
        with col1:
            fig, ax = plt.subplots()
            ax.imshow(dfwc)
            plt.axis('off')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.barh(popwords[0], popwords[1])
            plt.gca().invert_yaxis()
            st.pyplot(fig)




footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
color: red;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;'>Abhishek Gangwar</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
