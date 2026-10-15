# progress.py


def update_progress(progress_bar,progress_label, step, max_steps , label_text):
    progress_label.config(text=f'{label_text} {step+1} / {max_steps} 完了')
    progress_bar["value"] = (step / max_steps) * 100
    progress_bar.update()
