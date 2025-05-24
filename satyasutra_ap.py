import streamlit as st
import pickle
import numpy as np
import streamlit.components.v1 as components

# --- Custom CSS for Animations ---
def inject_css():
    st.markdown("""
    <style>
        .stApp {
            background: #0a0a23;
            color: white;
        }
        @keyframes rotate3d {
            from { transform: rotateY(0deg) rotateX(0deg);}
            to { transform: rotateY(360deg) rotateX(360deg);}
        }
        .hero-3d {
            width: 150px; height: 150px; margin: 0 auto 20px auto;
            perspective: 800px;
        }
        .object {
            width: 100%; height: 100%;
            background: rgba(76, 175, 80, 0.5);
            border-radius: 50%; border: 3px solid #4caf50;
            animation: rotate3d 20s linear infinite;
        }
        .subtitle {
            margin-top: 20px; font-size: 1.2rem;
            animation: fadeIn 3s ease forwards;
            animation-delay: 2.5s;
            text-align: center; max-width: 300px; color: white;
        }
        @keyframes fadeIn {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
    </style>
    """, unsafe_allow_html=True)

# --- Load the Model ---
@st.cache_resource
def load_model():
    # Update the path to your .sav file as needed
    return pickle.load(open('Satyasutra.sav', 'rb'))

model = load_model()

# --- Main App ---
def main():
    inject_css()
    st.markdown("<h1 style='text-align: center;'>SatyaSutra</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Protecting the truth from the spread of false</div>", unsafe_allow_html=True)

    # Hero Section with 3D Object
    components.html("""
    <div class="hero-3d">
        <div class="object"></div>
    </div>
    """, height=180)

    st.markdown("---")

    # Example: Text input for a fake news classifier
    st.markdown("### Enter text to analyze")
    with st.form("analysis_form"):
        user_input = st.text_area("Paste news/article/text here", height=150)
        submitted = st.form_submit_button("Analyze")

    if submitted and user_input:
        # Simulated progress bar
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            progress_bar.progress(percent_complete + 1)
        # --- Prediction (adjust as per your model's requirements) ---
        # If your model expects a list/array, wrap input as needed
        try:
            # For text models, you may need to preprocess or vectorize
            # Here we assume model.predict([user_input]) works
            prediction = model.predict([user_input])[0]
            # If your model provides probability/confidence
            if hasattr(model, "predict_proba"):
                confidence = np.max(model.predict_proba([user_input]))
            else:
                confidence = None
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            return

        # --- Animated Result Display ---
        if prediction == 1 or prediction == "True" or prediction == "truth":
            st.success(f"✅ Truth Verified" + (f" with {confidence*100:.1f}% Confidence" if confidence else ""))
            # Confetti animation
            components.html("""
            <div style="display: flex; justify-content: center; margin-top: 1rem;">
                <div style="width: 20px; height: 20px; background: #4caf50; margin: 0 2px; border-radius: 50%; animation: fadeIn 1s ease;"></div>
                <div style="width: 20px; height: 20px; background: #81c784; margin: 0 2px; border-radius: 50%; animation: fadeIn 1.2s ease;"></div>
                <div style="width: 20px; height: 20px; background: #388e3c; margin: 0 2px; border-radius: 50%; animation: fadeIn 1.4s ease;"></div>
            </div>
            """, height=40)
        else:
            st.error(f"❌ False/Unverified" + (f" with {confidence*100:.1f}% Confidence" if confidence else ""))
            # Red glow animation
            components.html("""
            <div style="display: flex; justify-content: center; margin-top: 1rem;">
                <div style="width: 20px; height: 20px; background: #f44336; margin: 0 2px; border-radius: 50%; animation: fadeIn 1s ease; box-shadow: 0 0 15px #f44336;"></div>
                <div style="width: 20px; height: 20px; background: #e57373; margin: 0 2px; border-radius: 50%; animation: fadeIn 1.2s ease; box-shadow: 0 0 10px #e57373;"></div>
                <div style="width: 20px; height: 20px; background: #b71c1c; margin: 0 2px; border-radius: 50%; animation: fadeIn 1.4s ease; box-shadow: 0 0 8px #b71c1c;"></div>
            </div>
            """, height=40)

main()
