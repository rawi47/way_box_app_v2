Authentication
##############

Nodogsplash v1 -Site-wide username and password
*******************************

Nodogsplash v1 and earlier can be configured to require a username and/or password to be
entered on the splash page as part of the authentication process. Since the
username and password are site-wide (not per user), and they are sent in the
clear using HTTP GET, this is not a secure mechanism.
To enable this, edit *nodogsplash.conf* to set parameters *PasswordAuthentication*,
*UsernameAuthentication*, *Password*, *Username*, and *PasswordAttempts* as desired.
Then the splash page must use a GET-method HTML form to send user-entered
username and/or password as values of variables *nodoguser* and *nodogpass*
respectively, along with others as required, to the server. For example:

.. code::

   <form method='GET' action='$authaction'>
   <input type='hidden' name='tok' value='$tok'>
   <input type='hidden' name='redir' value='$redir'>
   username: <input type='text' name='nodoguser' value='' size='12' maxlength='12'>
   <br>
   password: <input type='password' name='nodogpass' value='' size='12' maxlength='10'>
   <br>
   <input type='submit' value='Enter'>
   </form>

Nodogsplash ALL versions -Forwarding Authentication Service (FAS)
***************************************

Nodogsplash (NDS) can support external (to NDS) authentication.
The BinVoucher process was derived to support this and has been called Forwarding Authentication. This is a non trivial function and although partially implemented in early versions, is not implemented at all in version 2, at the time of writing.

Fortunately, Forwarding Authentication can be done without any modification to the core NDS code and in a way that is compatible with all versions, pre v1 beta through to the current release of v2.

The defacto industry standard Captive Portal Detection (CPD), present on almost all devices these days, invokes the NDS splash page with various parameters passed to the splash page by NDS, including the client access token.  

It is a simple matter to pass this token to an external Forwarding Authentication Service (FAS) by using a redirect in the splash page.

For a client to access this external service, the ip address and port number of the service must be added to the NDS walled garden in nodogsplash.conf or its equivalent UCI config file if running under LEDE/OpenWrt.

Included are various configuration files and remote php scripts, intended as an example implementation of FAS to demonstrate the methods.

FAS Installation
****************
NOTE: USING HTTPS. Your FAS can be an https server, but self signed certificates will throw dire "Here Be Dragons" warnings on your client devices when the redirection to your FAS takes place. Also even if using a registered CA all browsers will still return a security error on returning to Nodogsplash. This can be prevented by using wget to return to Nodogsplash from your FAS script instead of an html GET.

The contents of the FAS etc folder should be placed in the /etc folder of your NoDogSplash router, overwriting existing files.

The following two files should be edited as follows.

1:
/etc/config/nodogsplash should be edited to reflect the ip address and port of your FAS service as described in the comments in the example file.
Your FAS can reside on your Nodogsplash router, a web server on your LAN, or a web server on the internet. 

2:
/etc/nodogsplash/htdocs/splash.html should also be edited to reflect the URL of your FAS service as indicated in the comments in the example file.
Take note of the USING HTTPS warning above. A typical URL could be http://my-fas.net/nodog/fas.php?auth.... etc.

Running FAS on your Nodogsplash router:
The example FAS service will run fairly well on uhttpd (the web server that serves Luci) on an LEDE/OpenWrt supported device with 8MB flash and 32MB ram but shortage of ram may well be an issue if more than two or three clients log in at the same time. For this reason a device with a minimum of 16MB flash and 64MB ram is recommended.

Running on uhttpd:
Install the modules php7 and php7-cgi on LEDE for the simple example. Further modules may be required when you write your own php scripts depending on your requirements.
To enable php in uhttpd you must add the line:
	list interpreter ".php=/usr/bin/php-cgi"
to the /etc/config/uhttpd file in the config uhttpd 'main' or first section.

Finally, reboot the router to start NoDogSplash in FAS mode.

The example file "users.dat" contains a list of usernames and passwords.

NOTE: /etc/config/nodogsplash contains the line "option enabled 1". If you have done something wrong and locked yourself out, you can still SSH to your router and stop NoDogSplash (ndsctl stop) to fix the problem.
