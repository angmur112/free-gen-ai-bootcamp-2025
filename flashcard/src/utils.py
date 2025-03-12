import streamlit as st

def create_spaced_repetition_tracker():
    """
    Simple spaced repetition tracking
    """
    if 'vocabulary_progress' not in st.session_state:
        st.session_state.vocabulary_progress = {}
    
    return st.session_state.vocabulary_progress

def track_vocabulary_progress(vocab_item):
    """
    Track vocabulary learning progress
    """
    vocab_progress = create_spaced_repetition_tracker()
    
    if vocab_item['japanese'] not in vocab_progress:
        vocab_progress[vocab_item['japanese']] = {
            'attempts': 0,
            'correct': 0
        }
    
    vocab_progress[vocab_item['japanese']]['attempts'] += 1
    
    return vocab_progress