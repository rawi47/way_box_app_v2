from django.db import models
from ftplib import FTP
import ftplib

class FtpUtils(models.Model):


	def _connect_to_ftp(self,ftp_host,ftp_user,ftp_password):
		try:
			ftp = FTP(ftp_host,ftp_user,ftp_password)
			
			if not isinstance(ftp,FTP):
				ftp = FTP(ftp_host,ftp_user,ftp_password)    # connect to host, default port
			ftp.login() 
			
		except Exception as e:
			print(str(e))
		return ftp

	def _is_ftp_dir(self,ftp_handle, name, guess_by_extension=True):
	    """ simply determines if an item listed on the ftp server is a valid directory or not """

	    # if the name has a "." in the fourth to last position, its probably a file extension
	    # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
	    if guess_by_extension is True:
	        if name[-4] == '.':
	            return False

	    original_cwd = ftp_handle.pwd()     # remember the current working directory
	    try:
	        ftp_handle.cwd(name)            # try to set directory to new name
	        ftp_handle.cwd(original_cwd)    # set it back to what it was
	        return True
	    except:
	        return False


	def _make_parent_dir(self,fpath):
	    """ ensures the parent directory of a filepath exists """
	    dirname = os.path.dirname(fpath)
	    while not os.path.exists(dirname):
	        try:
	            os.mkdir(dirname)
	            print("created {0}".format(dirname))
	        except:
	            self._make_parent_dir(dirname)


	def _download_ftp_file(self,ftp_handle, name, dest, overwrite):
	    """ downloads a single file from an ftp server """
	    self._make_parent_dir(dest)
	    if not os.path.exists(dest) or overwrite is True:
	        with open(dest, 'wb') as f:
	            ftp_handle.retrbinary("RETR {0}".format(name), f.write)
	        print("downloaded: {0}".format(dest))
	    else:
	        print("already exists: {0}".format(dest))


	def _mirror_ftp_dir(self,ftp_handle, name, overwrite, guess_by_extension):
	    """ replicates a directory on an ftp server recursively """
	    for item in ftp_handle.nlst(name):
	        if self._is_ftp_dir(ftp_handle, item):
	            self._mirror_ftp_dir(ftp_handle, item, overwrite, guess_by_extension)
	        else:
	            self._download_ftp_file(ftp_handle, item, item, overwrite)


	def _download_ftp_tree(self,ftp_handle, path, destination, overwrite=True, guess_by_extension=True):
	    """
	    Downloads an entire directory tree from an ftp server to the local destination

	    :param ftp_handle: an authenticated ftplib.FTP instance
	    :param path: the folder on the ftp server to download
	    :param destination: the local directory to store the copied folder
	    :param overwrite: set to True to force re-download of all files, even if they appear to exist already
	    :param guess_by_extension: It takes a while to explicitly check if every item is a directory or a file.
	        if this flag is set to True, it will assume any file ending with a three character extension ".???" is
	        a file and not a directory. Set to False if some folders may have a "." in their names -4th position.
	    """
	    os.chdir(destination)
	    self._mirror_ftp_dir(ftp_handle, path, overwrite, guess_by_extension)	

	def _close_ftp(self,ftp):
		ftp.quit()
	
