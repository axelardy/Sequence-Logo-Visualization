from flask import Flask, render_template, request, redirect, url_for
import logomaker
import pandas as pd


colors_zip = {'A': '#b36139', 'C': '#ef0300', 'D': '#068855', 'E': '#028489', 'F': '#da06b6', 'G': '#797c00', 'H': '#0f73ee', 'I': '#ea0063', 'K': '#0a81a2', 'L': '#de1a76', 'M': '#a10c56', 'N': '#0f5e46', 'P': '#1c8701', 'Q': '#19577b', 'R': '#0a7dbc', 'S': '#6e5842', 'T': '#843f07', 'V': '#da3952', 'W': '#4600ff', 'Y': '#8607b4', 'B': '#FFFFFF', 'Z': '#FFFFFF', 'X': '#FFFFFF', '*': '#FFFFFF'}



print(colors_zip)

def processing(sequences):
    sequences,valSize,valSame = string2list(sequences)
    if not valSize:
        return render_template("error.html", error = "Sequences is more than 16" )
    elif not valSame:
        return render_template("error.html", error = "Sequences are not consistent in lenght" )
    drawlogo(sequences)
    return render_template("result.html", result = result)


def string2list(sequences):
    valSize = True
    valSame = True
    sequences = sequences.split('\n')
    sequences = [sequence.upper().strip('\r') for sequence in sequences if sequence != '']


    first_length = len(sequences[0]) if sequences else 0

    if len(sequences) > 16:
        valSize = False

    # Check if all sequences have the same length and length is less than 16
    for sequence in sequences:
        if len(sequence) != first_length :
            valSame = False
            break

    return sequences, valSize,valSame

def drawlogo(sequences):
    data = pd.DataFrame({char: [0]*len(sequences[0]) for char in 'ARNDCQEGHILKMFPSTWYV'})

    for sequence in sequences:
        for index, char in enumerate(sequence):
            data.loc[index, char] += 1
    data = data.div(data.sum(axis=1), axis=0)
    data = logomaker.transform_matrix(data, from_type='probability', to_type='information')

    logo = logomaker.Logo(data,color_scheme=colors_zip)

    logo.style_spines(visible=False)
    logo.style_spines(spines=['left', 'bottom'], visible=True)
    lenght = len(sequences[0])
    logo.ax.set_xlabel("Position")
    logo.ax.set_xticks(range(0, lenght))
    logo.ax.set_xticklabels(range(1, lenght+1))
    logo.ax.set_ylabel("Bits")

    # Save the logo
    logo.fig.savefig("static/output.svg")
    logo.fig.savefig("static/output.png")
    logo.fig.savefig("static/output.jpg")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        next_page = processing(result['sequence'])
        return next_page

if __name__ == '__main__':
    app.run()




