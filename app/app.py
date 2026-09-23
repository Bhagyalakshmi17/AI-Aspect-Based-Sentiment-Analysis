import streamlit as st
from aspect_sentiment import analyze_aspects

st.set_page_config(
    page_title="AI Aspect-Based Sentiment Analysis",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Aspect-Based Sentiment Analysis")

st.write(
    "Analyze customer reviews at the aspect level using Natural Language Processing."
)

st.caption(
    "Enter a product review and the AI will identify individual aspects "
    "and classify their sentiment as Positive or Negative."
)

st.divider()

review = st.text_area(
    "Enter your review:",
    placeholder="Example: The camera is excellent but the battery life is terrible.",
    height=150
)

if st.button("Analyze Sentiment"):

    if review.strip():

        with st.spinner("Analyzing review..."):
            results = analyze_aspects(review)

        if results:
            st.subheader("Analysis Results")

            for result in results:
                aspect = result["aspect"]
                sentiment = result["sentiment"]
                confidence = result["confidence"]

                st.write(f"### {aspect.title()}")

                if sentiment == "POSITIVE":
                    st.success(
                        f"😊 Positive — Confidence: {confidence}%"
                    )

                elif sentiment == "NEGATIVE":
                    st.error(
                        f"😞 Negative — Confidence: {confidence}%"
                    )

                else:
                    st.info(
                        f"😐 {sentiment} — Confidence: {confidence}%"
                    )

            # Summary section
            positive_count = sum(
                1 for result in results
                if result["sentiment"] == "POSITIVE"
            )

            negative_count = sum(
                1 for result in results
                if result["sentiment"] == "NEGATIVE"
            )

            st.divider()
            st.subheader("Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric("Aspects Detected", len(results))
            col2.metric("Positive", positive_count)
            col3.metric("Negative", negative_count)

        else:
            st.warning(
                "No known product aspects were detected in the review."
            )

    else:
        st.warning("Please enter a review first.")