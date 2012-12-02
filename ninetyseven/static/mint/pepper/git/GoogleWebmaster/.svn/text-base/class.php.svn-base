<?php
/******************************************************************************
 Pepper
 
 Developer		: Gregor Godberse
 Plug-in Name	: gWebmasterTools
 
 http://godberit.de/

 ******************************************************************************/
 
$installPepper = "GIT_gWebmasterTools";
	
class GIT_gWebmasterTools extends Pepper
{
	var $version	= 100;
	var $info		= array
	(
		'pepperName'	=> 'gWebmasterTools',
		'pepperUrl'		=> 'http://godberit.de',
		'pepperDesc'	=> 'Displays Stats from Google Webmaster Tools',
		'developerName'	=> 'Gregor Godbersen',
		'developerUrl'	=> 'http://godberit.de'
	);
	var $panes = array
	(
		'Google Stats' => array
		(
			'Errors',
			'Content',
			'Top queries',
			'External',
			'Site',
			
		)
	);
	var $prefs = array
	(
		'table' => ''
	);

	/**************************************************************************
	 isCompatible()
	 **************************************************************************/
	function isCompatible()
	{
		if ($this->Mint->version >= 120)
		{
			return array
			(
				'isCompatible'	=> true
			);
		}
		else
		{
			return array
			(
				'isCompatible'	=> false,
				'explanation'	=> '<p>This Pepper is only compatible with Mint 1.2 and higher.</p>'
		);
		}
	}
	
	/**************************************************************************
	 onDisplay()
	 **************************************************************************/


	function onDisplay($pane, $tab, $column = '', $sort = '')
	{
		$html = '';
		switch($pane) 
		{
			case 'Google Stats':
				switch($tab)
				{
					case 'Errors':
						$html .= $this->getHTML_showFrame('https://www.google.com/webmasters/tools/crawlerrors_gadget');
						break;
					case 'Content':
						$html .= $this->getHTML_showFrame('https://www.google.com/webmasters/tools/contentproblems_gadget');
						break;
					case 'Top queries':
						$html .= $this->getHTML_showFrame('https://www.google.com/webmasters/tools/topsearchqueries_gadget');
						break;
					case 'External':
						$html .= $this->getHTML_showFrame('https://www.google.com/webmasters/tools/externallinks_gadget');
						break;
					case 'Site':
						$html .= $this->getHTML_showFrame('https://www.google.com/webmasters/tools/sitelinks_gadget');
						break;	
			
					default:
					 $html .= $this->getHTML_Error('UI Fail');
					break;
				}
			break;
		}
		return $html;
	}
	
	/**************************************************************************
	 onDisplayPreferences()
	 **************************************************************************/
	/* function onDisplayPreferences() 
	{
		

		
		//return null;
	}
	
	
	function onSavePreferences() 
	{
		//$this->prefs['table'] = $this->escapeSQL($_POST['table']);
	}
	
	function querydOamo($url){
		return file_get_contents($url);
	}
	*/
	function getHTML_showFrame($url)
	{
		
		$data = '<iframe style="height:240px;width:100%;border:0;" src="'.$url.'"></iframe>';
		return $data;
	}
	
	
	
	function getHTML_Error($msg, $checkSettings = false)
	{
		$html = "<div style='line-height: 2em; text-align: center;'><strong>{$msg}</strong>";
		if ($checkSettings)
		{
			$html .= "<br />Please check your settings in:<br /><code>pepper/git/GoogleWebmaster/class.php</code>";
		}
		$html .= "</div>";
		
		return $html;
	}
}