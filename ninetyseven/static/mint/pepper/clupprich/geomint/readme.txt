================================================================================
PEPPER MAKES MINT BETTER

Installing GeoMint 0.55
--------------------------------------------------------------------------------

IMPORTANT: To use GeoMint, you need the Secret Crush Pepper installed (can be found at http://haveamint.com)

1. Create a directory 'clupprich' in /mint/pepper/.

2. Create a directory 'geomint' in /mint/pepper/clupprich/.

3. Upload the class.php and blank.gif into that new folder.
   It should then look something like
   /mint/pepper/clupprich/geomint/class.php
   and
   /mint/pepper/clupprich/geomint/blank.gif

4. Go to your pepper preferences window and backup your data (NOT only configuration).
   GeoMint won't damage your data, however, it's better to be on the safe side.
   You can now install GeoMint.
   
5. Tweak your settings and enjoy!

6. ONLY IF YOU ARE UPDATING FROM GEOMINT VERSION 0.50:
   Edit the display.php in your /mint/app/paths/display/ directory and DELETE the following line:

   <script type="text/javascript" src="http://maps.google.com/maps?file=api&v=2&key=___YOUR_API_KEY___">//Google API</script>
   
   Substitute ___YOUR_API_KEY___ with your Google Maps API key
   (stored in the Mint preferences when you're updating from a previous version of GeoMint).

================================================================================
Copyright 2005-2007 Christoph Lupprich.
Credits also go to Geoffrey Hughes (various features).

More info will is available at http://www.stopbeingcarbon.com/geomint
