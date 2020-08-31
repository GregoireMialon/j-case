from flask import Flask, render_template, request
from wtforms import Form, validators, StringField
from mol_back import MoleculeParser

application = Flask(__name__)

def parse_molecule(molecule):
    parser = MoleculeParser()
    return parser.output(molecule)

# Model
class InputForm(Form):
    r = StringField(validators=[validators.InputRequired()])

# View
@application.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        r = form.r.data
        s = parse_molecule(r)
        return render_template("view_output.html", form=form, s=s)
    else:
        return render_template("view_input.html", form=form)

if __name__ == '__main__':
    application.run(debug=True)