#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

# from flask import render_template
# from flask_uploads import TEXT, UploadSet
# from flask_wtf import Form
# from flask_wtf.file import FileField, FileAllowed, FileRequired
# from wtforms import SubmitField
#
# from ..__init__ import app
#
# set_txt = UploadSet('txt', TEXT)
#
#
# class UploadForm(Form):
#     '''
#         一个简单的上传表单
#     '''
#
#     # 文件field设置为‘必须的’，过滤规则设置为‘set_txt’
#     upload = FileField('image', validators=[FileRequired(), FileAllowed(set_txt, 'you can upload txt only!')])
#     submit = SubmitField('ok')
#
#
# @app.route('/upload', methods=('GET', 'POST'))
# def upload():
#     form = UploadForm()
#     url = None
#     if form.validate_on_submit():
#         filename = form.upload.data.filename
#         url = set_txt.save(form.upload.data, name=filename)
#     return render_template('upload.html', form=form, url=url)
#
