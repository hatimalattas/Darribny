from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, AnyOf


class ReveiwForm(FlaskForm):
    rate = SelectField('Rate',
                          choices=[(5, '⭐️⭐️⭐️⭐️⭐️ Excellent'), (4, '⭐️⭐️⭐️⭐️ Great'), (3, '⭐️⭐️⭐️ Okay'), (2, '⭐️⭐ Bad'),  (1, '⭐️ Very Bad')], validators= [AnyOf(values=[1,2,3,4,5], message='Please rate')])
    comment = TextAreaField('Comment', render_kw={"placeholder": 'Write a comment'})
    submit = SubmitField('Submit')

    