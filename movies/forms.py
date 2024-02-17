from django import forms
from django.core.validators import validate_email
import json

class ShortsVideoCreatorForm(forms.Form):
    title = forms.CharField(label='제목', max_length=100)
    voice_id = forms.CharField(label='클론 목소리 ID', max_length=100)
    videos_info = forms.CharField(widget=forms.HiddenInput(), required=False, label='비디오 정보')
    intro_text = forms.CharField(widget=forms.Textarea, label='인트로 텍스트', required=False)
    outro_text = forms.CharField(widget=forms.Textarea, label='아웃트로 텍스트', required=False)
    background_mp3 = forms.FileField(label='배경 음악 파일', required=False)
    intro_video_file = forms.FileField(label='인트로 비디오 파일', required=False)
    outro_video_file = forms.FileField(label='아웃트로 비디오 파일', required=False)

    def clean_videos_info(self):
        videos_info = self.cleaned_data.get('videos_info', '{}')  # 기본값을 '{}'로 설정
        try:
            videos_info_json = json.loads(videos_info)
        except json.JSONDecodeError:
            raise forms.ValidationError('비디오 정보가 올바른 JSON 형식이 아닙니다.')
        return videos_info_json