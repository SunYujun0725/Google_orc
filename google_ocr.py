#!/usr/bin/python3
from __future__ import print_function
from googleapiclient.errors import HttpError
import httplib2
import os
import io
import cv2
import numpy as np
import time
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Python OCR'
def enhance(img: np.ndarray) -> np.ndarray:
    """
    params img: input image
    return: enhanced image in grayscale
    """
    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img2 = cv2.resize(img2, (256, 256))
    ret, th2 = cv2.threshold(img2, 100, 255, cv2.THRESH_BINARY_INV)   
    # erode and dilation
    kernel = np.ones((3, 3), np.uint8)
    th2 = cv2.erode(th2, kernel, iterations=2)
    th2 = cv2.dilate(th2, kernel, iterations=2)
    return th2

def get_credentials():
  """取得有效的憑證
     若沒有憑證，或是已儲存的憑證無效，就會自動取得新憑證

     傳回值：取得的憑證
  """
  credential_path = os.path.join("./", 'google-ocr-credential.json')
  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
      credentials = tools.run(flow, store)
    print('憑證儲存於：' + credential_path)
  return credentials

def main():

  try:  
    # 取得憑證、認證、建立 Google 雲端硬碟 API 服務物件
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    #放有不同風個的目錄
    dir = './zmf_complete'

    '''
    for filename in os.listdir(dir):
      dic2 = dir + '/' + filename
      for filename2 in os.listdir(dic2):
        # 包含文字內容的圖片檔案(png、jpg、bmp、gif、pdf)
        if not filename2[0].isdigit():
          # print('hi'+filename2)
          continue
        imgfile = dic2 +'/' +filename2
        # 輸出辨識結果的文字檔案
        txtfile = 'output.txt'
        # 上傳成 Google 文件檔，讓 Google 雲端硬碟自動辨識文字
        mime = 'application/vnd.google-apps.document'
        res = service.files().create(
          body={
            'name': imgfile,
            'mimeType': mime
          },
          media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)).execute()

        # 下載辨識結果，儲存為文字檔案
        downloader = MediaIoBaseDownload(
        io.FileIO(txtfile, 'wb'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
          status, done = downloader.next_chunk()

        # 刪除剛剛上傳的 Google 文件檔案
        service.files().delete(fileId=res['id']).execute()

        # 建立相同圖片，但重新命名為文字辨識的結果

        # 打开文本文件，指定编码方式
        with open('output.txt', 'r', encoding='utf-8') as file:
          # 读取文本内容
          content = file.read()
        # 获取特定位置的中文字
        if(len(content) > 19):
          chi_char = content[19]
        else:
          chi_char = 'w'#表示沒有辨識到字
        img = cv2.imread(imgfile)
        img_name = dic2 + '/' + chi_char + '_'+ filename2
        cv2.imwrite(img_name, img)
        # 刪除本地端檔案
        os.remove(imgfile)
    '''
        
    dic2 = dir
    for filename2 in os.listdir(dic2):
        # 包含文字內容的圖片檔案（png、jpg、bmp、gif、pdf）
        if not filename2[0].isdigit():
          # print('hi'+filename2)
          continue
        imgfile = dic2 +'/' +filename2
        # 輸出辨識結果的文字檔案
        txtfile = 'output.txt'
        # 上傳成 Google 文件檔，讓 Google 雲端硬碟自動辨識文字
        mime = 'application/vnd.google-apps.document'
        res = service.files().create(
          body={
            'name': imgfile,
            'mimeType': mime
          },
          media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)).execute()

        # 下載辨識結果，儲存為文字檔案
        downloader = MediaIoBaseDownload(
        io.FileIO(txtfile, 'wb'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
          status, done = downloader.next_chunk()

        # 刪除剛剛上傳的 Google 文件檔案
        service.files().delete(fileId=res['id']).execute()

        # 建立相同圖片，但重新命名為文字辨識的結果

        # 打开文本文件，指定编码方式
        with open('output.txt', 'r', encoding='utf-8') as file:
          # 读取文本内容
          content = file.read()
        # 获取特定位置的中文字
        if(len(content) > 19):
          chi_char = content[19]
        else:
          chi_char = 'w'#表示沒有辨識到字
        img = cv2.imread(imgfile)
        img_name = dic2 + '/' + chi_char + '_'+ filename2
        cv2.imwrite(img_name, img)
        # 刪除本地端檔案
        os.remove(imgfile)

  except HttpError as err:
    # If the error is a rate limit or connection error,
    # wait and try again.
    if err.resp.status in [403, 500, 503]:
      time.sleep(5)
    else: raise
if __name__ == '__main__':
  main()