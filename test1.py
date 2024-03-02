from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


try:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
except Exception as _ex:
    print('Wrong email address. Please, check your email address and try again!')


def create_and_upload_file(file_name='test.txt', file_content='Hey Dude'):

    try:
        drive = GoogleDrive(gauth)

        my_file = drive.CreateFile({'title': f'{file_name}'})
        my_file.SetContentString(file_content)
        my_file.Upload()

        return f'File {file_name} was uploaded! Have a good day!'
    except Exception as _ex:
        return "Got some trouble, check your code please"


def download_file(file_name='', file_path=''):
    pass


def main():
    # print(create_and_upload_file(file_name='hello.txt', file_content='Hello friend'))
    print(download_file())


if __name__ == '__main__':
    main()
