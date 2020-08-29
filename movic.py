from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidget, QFileDialog, QTableWidgetItem, QColorDialog, \
    QProgressBar, QStatusBar
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWebEngineWidgets import QWebEngineView

import moviepy.editor as me
from moviepy.video.io.preview import preview

import pygame as py
import os
import cv2


class MainWin:
    def __init__(self):
        qfile = QFile('main.ui')
        qfile.open(qfile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.ui.setWindowTitle('movic')
        # 视频
        self.clips = []
        self.names = []
        self.filepaths = []
        # 字幕颜色
        self.color = 'white'

        # self.ui.open_button.clicked.connect(self.open_button)
        # self.ui.save_button.clicked.connect(self.save_button)
        self.ui.actionopen.triggered.connect(self.open_button)
        self.ui.actionsave.triggered.connect(self.save_button)
        self.ui.preview_button.clicked.connect(self.preview_button)
        self.ui.silence_button.clicked.connect(self.silence_button)
        self.ui.back_button.clicked.connect(self.back_button)
        self.ui.x_mirror_button.clicked.connect(self.x_mirror_button)
        self.ui.y_mirror_button.clicked.connect(self.y_mirror_button)
        self.ui.speed_button.clicked.connect(self.speed_button)
        self.ui.size_button.clicked.connect(self.size_button)
        self.ui.light_button.clicked.connect(self.light_button)
        self.ui.sub_button.clicked.connect(self.sub_button)
        self.ui.connect_button.clicked.connect(self.connect_button)
        self.ui.music_connect_button.clicked.connect(self.music_connect_button)
        self.ui.inc_music_button.clicked.connect(self.inc_music_button)
        self.ui.pic2video_button.clicked.connect(self.pic2video_button)
        self.ui.video2pic_button.clicked.connect(self.video2pic_button)
        self.ui.pic_music_button.clicked.connect(self.pic_music_button)
        self.ui.volumex_button.clicked.connect(self.volumex_button)
        self.ui.clips_button.clicked.connect(self.clips_button)
        self.ui.fontcolor_button.clicked.connect(self.fontcolor_button)
        self.ui.font_insert_button.clicked.connect(self.font_insert_button)

    def open_button(self):
        filepath = QFileDialog.getOpenFileName(self.ui, "请选择需要打开的文件",
                                               r'c:/',
                                               '文件 (*.mp4);;文件 (*.avi);;文件 (*.wmv);;文件 (*.rm);;文件 (*.rmvb);;文件 (*.mkv);;文件 (*.mov);;文件 (*.m4v);;文件 (*.3gp);;文件 (*.gif);;文件 (*.mp3);;文件 (*.wav);;文件 (*.mpeg);;文件 (*.wma);;文件 (*.flac)')

        if filepath[0].split('.')[-1] in ['mp4', 'avi', 'wmv', 'rm', 'rmvb', 'mov', 'm4v', '3gp', 'webm', 'mkv']:
            name = filepath[0].split('/')[-1]
            self.names.append(name)
            self.filepaths.append(filepath[0])
            self.ui.filename_cbox.addItem(name)
            self.clips.append(me.VideoFileClip(filepath[0]))
            x, y, z = self.clips[self.names.index(name)].duration, self.clips[self.names.index(name)].size[0], self.clips[self.names.index(name)].size[1]
            info = f'{name}:时长{x}s:长{y}px:宽:{z}px'
            self.ui.file_info.append(info)
            QMessageBox.about(self.ui, '文件导入成功', '请进行下一步操作')
        elif filepath[0].split('.')[-1] in ['mp3', 'wav', 'mpeg', 'wma', 'flac']:
            name = filepath[0].split('/')[-1]
            self.names.append(name)
            self.filepaths.append(filepath[0])
            self.ui.filename_cbox.addItem(name)
            self.clips.append(me.AudioFileClip(filepath[0]))
            x = self.clips[self.names.index(name)].duration
            info = f'{name}:时长{x}s'
            self.ui.file_info.append(info)
            QMessageBox.about(self.ui, '文件导入成功', '请进行下一步操作')
        elif not filepath[0]:
            pass
        else:
            QMessageBox.critical(self.ui, '错误', '请选择正确的格式！')

    def save_button(self):
        filepath = QFileDialog.getSaveFileName(self.ui, "保存文件",
                                               r'c:/',
                                               '文件 (*.mp4);;文件 (*.webm);;文件 (*.gif);;文件 (*.mp3);;文件 (*.wav)')
        name = self.ui.filename_cbox.currentText()
        if filepath[0].split('.')[-1] in ['mp4', 'webm']:
            self.clips[self.names.index(name)].write_videofile(filepath[0])
            QMessageBox.about(self.ui, '文件保存成功', '请进行下一步操作')
            self.ui.file_info.append(f'{name}保存成功')
        elif filepath[0].split('.')[-1] in ['mp3', 'wav']:
            self.clips[self.names.index(name)].write_audioile(filepath[0])
            self.ui.file_info.append(f'{name}保存成功')
            QMessageBox.about(self.ui, '文件保存成功', '请进行下一步操作')
        elif filepath[0].split('.')[-1] == 'gif':
            self.clips[self.names.index(name)].write_gif(filepath[0])
            self.ui.file_info.append(f'{name}保存成功')
            QMessageBox.about(self.ui, '文件保存成功', '请进行下一步操作')
        elif not filepath[0]:
            pass
        else:
            QMessageBox.critical(self.ui, '错误', '请选择正确的格式！')

    def preview_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            event = self.clips[self.names.index(name)].preview()
            e_list = []
            for each in event:
                t = str(each['time'])
                rgb = str(list(each['color']))
                position = str(each['position'])
                e_list.append(f'点击处：时间 {t}，位置 {position}，rgb {rgb}')
            for each in e_list:
                self.ui.file_info.append(each)
            py.quit()
            # sys.exit()
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')
        except AttributeError:
            QMessageBox.critical(self.ui, '错误', '音频文件和拼接文件不能预览！')

    def silence_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].set_audio(0)
            self.ui.file_info.append(f'{name}完成了静音操作')
            QMessageBox.about(self.ui, '静音成功', '请进行下一步操作')
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')
        except AttributeError:
            QMessageBox.critical(self.ui, '错误', '音频文件不能静音！')

    def back_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].fx(me.vfx.time_mirror)
            self.ui.file_info.append(f'{name}完成了倒放操作')
            QMessageBox.about(self.ui, '倒放成功', '请进行下一步操作')
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')

    def x_mirror_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].fx(me.vfx.mirror_x)
            self.ui.file_info.append(f'{name}完成了x轴镜像操作')
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')
        except AttributeError:
            QMessageBox.critical(self.ui, '错误', '音频文件不能镜像！')

    def y_mirror_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].fx(me.vfx.mirror_y)
            self.ui.file_info.append(f'{name}完成了y轴镜像操作')
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')
        except AttributeError:
            QMessageBox.critical(self.ui, '错误', '音频文件不能镜像！')

    def speed_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            speed_num = self.ui.speed_cbox.currentText()[:-2]
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].fx(me.vfx.speedx, float(speed_num))
            self.ui.file_info.append(f'{name}完成了{speed_num}倍速操作')
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError:
            QMessageBox.critical(self.ui, '错误', '请先导入视频文件！')

    def size_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            h, w = self.ui.size_line.text().split()
            int(h)
            try:
                self.clips[self.names.index(name)] = self.clips[self.names.index(name)].resize([int(h), int(w)])
                self.ui.file_info.append(f'{name}完成了重置大小操作,目前大小为（{h},{w}）')
                self.ui.size_line.clear()
                QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
            except AttributeError:
                self.ui.size_line.clear()
                QMessageBox.critical(self.ui, '错误', '音频文件不能调整画面！')
        except ValueError as v:
            if str(v) == "'' is not in list":
                self.ui.size_line.clear()
                QMessageBox.critical(self.ui, '错误', '请先导入文件！')
            else:
                self.ui.size_line.clear()
                QMessageBox.critical(self.ui, '错误', '请分别输入正确的视频画面长度和高度！')
        except (TypeError, SyntaxError):
            self.ui.size_line.clear()
            QMessageBox.critical(self.ui, '错误', '请分别输入正确的视频画面长度和高度！')

    def light_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            light_num = self.ui.light_line.text()
            float(light_num)
            try:
                self.clips[self.names.index(name)] = self.clips[self.names.index(name)].fx(me.vfx.colorx, float(light_num))
                self.ui.file_info.append(f'{name}完成了调节明暗操作,倍数为{light_num}')
                self.ui.light_line.clear()
                QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
            except AttributeError:
                self.ui.light_line.clear()
                QMessageBox.critical(self.ui, '错误', '音频文件不能调整画面！')
        except ValueError as v:
            if str(v) == "'' is not in list":
                self.ui.light_line.clear()
                QMessageBox.critical(self.ui, '错误', '请先导入文件！')
            else:
                self.ui.light_line.clear()
                QMessageBox.critical(self.ui, '错误', '请输入正确数值！')
        except (TypeError, SyntaxError):
            self.ui.light_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确数值！')

    def sub_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            sub1, sub2 = self.ui.sub_line.text().split()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].subclip(float(sub1), float(sub2))
            self.ui.file_info.append(f'{name}完成了截取操作,截取时间段为{sub1}s~{sub2}s')
            self.ui.sub_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError as v:
            if str(v) == "'' is not in list":
                self.ui.sub_line.clear()
                QMessageBox.critical(self.ui, '错误', '请先导入文件！')
            else:
                self.ui.sub_line.clear()
                QMessageBox.critical(self.ui, '错误', '请输入正确的起始时间和结束时间！')
        except (TypeError, SyntaxError):
            self.ui.sub_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的起始时间和结束时间！')

    def connect_button(self):
        connect_list = []
        name = ''
        try:
            for each in self.ui.connect_line.text().split():
                connect_list.append(self.clips[int(each) - 1])
                name += self.names[int(each) - 1]
            self.clips.append(me.CompositeVideoClip(connect_list))
            self.names.append(name)
            self.filepaths.append('')
            self.ui.filename_cbox.addItem(name)
            self.ui.file_info.append(f'新文件{name}已生成')
            self.ui.connect_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except (ValueError, TypeError, SyntaxError, IndexError):
            self.ui.connect_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的视频序号！')
        except AttributeError:
            self.ui.connect_line.clear()
            QMessageBox.critical(self.ui, '错误', '请选择视频文件！')

    def music_connect_button(self):
        connect_list = []
        name = ''
        try:
            for each in self.ui.music_connect_line.text().split():
                connect_list.append(self.clips[int(each) - 1])
                name += self.names[int(each) - 1]
            self.clips.append(me.concatenate_audioclips(connect_list))
            self.names.append(name)
            self.filepaths.append('')
            self.ui.filename_cbox.addItem(name)
            self.ui.file_info.append(f'新文件{name}已生成')
            self.ui.music_connect_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except (ValueError, TypeError, SyntaxError, IndexError):
            self.ui.music_connect_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的音频序号！')
        except AttributeError:
            self.ui.music_connect_line.clear()
            QMessageBox.critical(self.ui, '错误', '请选择音频文件！')

    def inc_music_button(self):
        music_list = []
        flag = 1
        try:
            for each in self.ui.inc_music_line.text().split():
                music_list.append(self.clips[int(each) - 1])
            if len(music_list) > 1:
                try:
                    m = me.concatenate_audioclips(music_list)
                except AttributeError:
                    flag = 0
                    self.ui.inc_music_line.clear()
                    QMessageBox.critical(self.ui, '错误', '请选择音频文件！')
            else:
                try:
                    m = music_list[0]
                    m.nchannels
                except AttributeError:
                    flag = 0
                    self.ui.inc_music_line.clear()
                    QMessageBox.critical(self.ui, '错误', '请选择音频文件！')
        except (ValueError, TypeError, SyntaxError, IndexError):
            flag = 0
            self.ui.inc_music_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的音频序号！')

        if flag:
            name = self.ui.filename_cbox.currentText()
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].set_audio(m)
            self.ui.file_info.append(f'{name}添加背景音乐成功')
            self.ui.inc_music_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')

    def pic2video_button(self):
        try:
            filepath = QFileDialog.getExistingDirectory(self.ui, "选择图片路径", r'c:/')
            pic_list = os.listdir(filepath)
            try:
                f = self.ui.pic2video_line.text()
                if not f:
                    f = 25
                f = int(f)
                pic_list = list(map(lambda x: filepath + '/' + x, pic_list))

                try:
                    self.clips.append(me.ImageSequenceClip(pic_list, fps=f))
                    name = pic_list[0].split('/')[-1].split('.')[0] + '.mp4'
                    self.names.append(name)
                    self.ui.filename_cbox.addItem(name)
                    self.ui.file_info.append(f'新视频文件{name}已生成，文件来源为{filepath}')
                    self.ui.pic2video_line.clear()
                    QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
                except Exception as e:
                    if str(e) == "Moviepy: ImageSequenceClip requires all images to be the same size":
                        self.ui.pic2video_line.clear()
                        QMessageBox.critical(self.ui, '错误', '图片尺寸需一致！')

            except (ValueError, TypeError, SyntaxError):
                self.ui.pic2video_line.clear()
                QMessageBox.critical(self.ui, '错误', '请输入正确的帧数！')
        except FileNotFoundError:
            pass

    def video2pic_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            video_path = self.filepaths[self.names.index(name)]
            if not video_path:
                QMessageBox.critical(self.ui, '错误', '合成的视频无法直接导出成图片。请先保存视频，重新导入视频后再尝试！')
            else:
                choice = QMessageBox.question(
                        self.ui,
                        '确认',
                        '请确保视频未剪切，否则导出的图片的来源为原视频')
                if choice == QMessageBox.Yes:
                    filepath = QFileDialog.getExistingDirectory(self.ui, "选择图片保存路径", r'c:/')
                    try:
                        p = self.ui.video2pic_line.text()
                        if not p:
                            p = 1
                        p = int(p)
                        vc = cv2.VideoCapture(video_path)
                        count = 1
                        if vc.isOpened():
                            ret, frame = vc.read()
                        else:
                            ret = False
                        while ret:
                            ret, frame = vc.read()
                            if count % p == 0:
                                try:
                                    cv2.imwrite(filepath + '/' + str(count) + '.png', frame)
                                except:
                                    pass
                            count += 1
                            cv2.waitKey(1)
                        vc.release()
                        self.ui.file_info.append(f'文件{name}导出图片成功，图片文件位置为{filepath}')
                        self.ui.video2pic_line.clear()
                        QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
                    except (ValueError, TypeError, SyntaxError):
                        self.ui.video2pic_line.clear()
                        QMessageBox.critical(self.ui, '错误', '请输入正确的帧数！')
                else:
                    pass
        except ValueError:
            self.ui.video2pic_line.clear()
            QMessageBox.critical(self.ui, '错误', '请先导入视频！')

    def pic_music_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            self.clips.append(self.clips[self.names.index(name)].audio)
            new_name = name + '_bgm'
            self.names.append(new_name)
            self.ui.filename_cbox.addItem(new_name)
            self.ui.file_info.append(f'视频文件{name}音频提取成功，音频{new_name}')
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError as v:
            if str(v) == "'' is not in list":
                QMessageBox.critical(self.ui, '错误', '请先导入文件！')
        except AttributeError:
            QMessageBox.critical(self.ui, '错误', '请选择视频文件！')

    def volumex_button(self):
        try:
            name = self.ui.filename_cbox.currentText()
            v = self.ui.volumex_line.text()
            float(v)
            if not v:
                v = 1
            self.clips[self.names.index(name)] = self.clips[self.names.index(name)].volumex(float(v))
            self.ui.file_info.append(f'文件{name}音量调节成功，音量为原件的{v}')
            self.ui.volumex_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except ValueError as v:
            if str(v) == "'' is not in list":
                self.ui.volumex_line.clear()
                QMessageBox.critical(self.ui, '错误', '请先导入文件！')
            else:
                self.ui.volumex_line.clear()
                QMessageBox.critical(self.ui, '错误', '请输入正确数值！')
        except (TypeError, SyntaxError):
            self.ui.volumex_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确数值！')

    def clips_button(self):
        choice = self.ui.clips_cbox.currentText()
        connect_list = []
        name = ''
        try:
            if choice == '水平拼接':
                for each in self.ui.clips_line.text().split():
                    connect_list.append(self.clips[int(each) - 1])
                    name += self.names[int(each) - 1]
                self.clips.append(me.clips_array([connect_list]))
            elif choice == '垂直拼接':
                for each in self.ui.clips_line.text().split():
                    connect_list.append([self.clips[int(each) - 1]])
                    name += self.names[int(each) - 1]
                self.clips.append(me.clips_array(connect_list))
            else:
                total = []
                for x in range(len(self.ui.clips_line.text().split(','))):
                    for y in self.ui.clips_line.text().split(',')[x].split():
                        connect_list.append(self.clips[int(y) - 1])
                        name += self.names[int(y) - 1]
                    total.append(connect_list)
                    connect_list = []
                self.clips.append(me.clips_array(total))
            self.names.append(name)
            self.filepaths.append('')
            self.ui.filename_cbox.addItem(name)
            self.ui.file_info.append(f'新文件{name}已生成')
            self.ui.clips_line.clear()
            QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
        except (ValueError, TypeError, SyntaxError, IndexError):
            self.ui.clips_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的视频序号！')
        except AttributeError:
            self.ui.clips_line.clear()
            QMessageBox.critical(self.ui, '错误', '请选择视频文件！')

    def fontcolor_button(self):
        color = QColorDialog.getColor()
        self.color = color.name()

    def font_insert_button(self):
        # text_font = self.ui.font_cbox.currentText()
        text = self.ui.font_text.toPlainText()
        try:
            name = self.ui.filename_cbox.currentText()
            time_start, time_end = self.ui.font_line.text().split()
            duration = float(time_end) - float(time_start)
            pos = self.ui.pos_cbox.currentText()
            size = self.ui.font_size_cbox.currentText()
            text_insert = me.TextClip(text, font='SimHei', fontsize=int(size), color=self.color).set_position(pos).set_duration(duration)
            try:
                self.clips[self.names.index(name)].size
                self.clips[self.names.index(name)] = me.CompositeVideoClip([self.clips[self.names.index(name)], text_insert.set_start(int(time_start))])
                self.clips[self.names.index(name)].write_videofile('s.mp4')
                self.ui.file_info.append(f'文件{name}添加字幕成功，内容：{text}')
                self.ui.font_line.clear()
                self.ui.font_text.clear()
                QMessageBox.about(self.ui, '操作成功', '请进行下一步操作')
            except ValueError as v:
                if str(v) == "'' is not in list":
                    self.ui.font_line.clear()
                    QMessageBox.critical(self.ui, '错误', '请先导入文件！')
            except AttributeError:
                self.ui.font_line.clear()
                QMessageBox.critical(self.ui, '错误', '请选择视频文件！')
        except (ValueError, TypeError, SyntaxError):
            self.ui.font_line.clear()
            QMessageBox.critical(self.ui, '错误', '请输入正确的字幕插入时间！')


app = QApplication([])
app.setWindowIcon(QIcon('ico.png'))
mainwin = MainWin()
mainwin.ui.show()
app.exec_()