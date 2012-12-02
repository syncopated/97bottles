<?php
/******************************************************************************
 Pepper
 
 Developer: Ronald Heft
 Plug-in Name: Feedburner
 
 http://cavemonkey50.com/code/feedburner/
 
 ******************************************************************************/
if (!defined('MINT')) { header('Location:/'); }; // Prevent viewing this file 
$installPepper = "RH_Feedburner";
	
class RH_Feedburner extends Pepper
{
	var $version	= 203; 
	var $info		= array
	(
		'pepperName'	=> 'Feedburner',
		'pepperUrl'		=> 'http://cavemonkey50.com/code/feedburner/',
		'pepperDesc'	=> 'This Pepper will display Feedburner feed statistics within Mint.',
		'developerName'	=> 'Ronald Heft',
		'developerUrl'	=> 'http://cavemonkey50.com/'
	);
	var $panes = array
	(
		'Feedburner' => array
		(
			'Overview',
			'Past Week',
			'Past Month',
			'Past Year'
		),
		'Feedburner Items' => array
		(
			'Refresh'
		)
	);
	var $oddPanes	= array
	(
		'Feedburner'
	);
	var $prefs = array
	(
		'feed' => '',
		'api' => 'http://api.feedburner.com/awareness/1.0/',
		'cache' => 0,
		'cachetime' => 2
	);
	
	/**************************************************************************
	 isCompatible()
	 **************************************************************************/
	function isCompatible()
	{
		if ($this->Mint->version < 200)
		{
			$compatible = array
			(
				'isCompatible'	=> false,
				'explanation'	=> '<p>This Pepper requires Mint 2, a paid upgrade, now available at <a href="http://www.haveamint.com/">haveamint.com</a>.</p>'
			);
		}
		else
		{
			$compatible = array
			(
				'isCompatible'	=> true,
			);
		}
		return $compatible;
	}
	
	
	/**************************************************************************
	 onDisplay()
	 **************************************************************************/
	function onDisplay($pane, $tab, $column = '', $sort = '')
	{
		$html = '';
		
		switch($pane) 
		{
			case 'Feedburner': 
				switch($tab) 
				{
					case 'Overview':
						$html .= $this->getHTML_Overview();
					break;
					case 'Past Week':
						$html .= $this->getHTML_Week();
					break;
					case 'Past Month':
						$html .= $this->getHTML_Month();
					break;
					case 'Past Year':
						$html .= $this->getHTML_Year();
					break;
				}
				break;
			case 'Feedburner Items': 
				switch($tab) 
				{
					case 'Refresh':
						$html .= $this->getHTML_Items();
					break;
				}
				break;
		}
		return $html;
	}
	
	/**************************************************************************
	 onDisplayPreferences()
	 **************************************************************************/
	function onDisplayPreferences() 
	{
		$preferences = array();
		$prefs = $this->prefs;

		if (isset($this->Mint->cfg['pepperLookUp']['RH_Feedburner']))
		{
			$preferences['Feedburner IDs'] = <<<HERE
			<table>
				<tr>
					<td><label>Feedburner IDs</label></td>
					<td><span><input type='text' id='feed' name='feed' rows='6' cols='30' value='{$prefs['feed']}' /></span></td>
				</tr>
				<tr>
					<td colspan='2'>Enter your Feedburner ID. To track multiple feeds, separate the IDs with commas. Example: ronaldheft, ronaldheft/comments, LaG</td>
				</tr>
			</table>
HERE;
		$checked = ($prefs['api'] == 'https://feedburner.google.com/api/awareness/1.0/') ? ' checked="checked"':'';
		$preferences['Feedburner API'] = <<<HERE
		<table class='snug'>
			<tr>
				<td><input type="checkbox" id="api" name="api" class="cinch" value="0"$checked /> <label>Use Google API</label></td>
			</tr>
			<tr>
				<td>If you receive the message <strong>Error: (1) Feed Not Found</strong>, try enabling this checkbox. This will put you on Google's new API address.</td>
			</tr>
		</table>
HERE;
		$checked = ($prefs['cache'])?' checked="checked"':'';
		$preferences['Cache'] = <<<HERE
		<table class='snug'>
			<tr>
				<td><input type="checkbox" id="cache" name="cache" class="cinch" value="0"$checked /> <label>Enable Cache</label></td>
			</tr>
			<tr>
				<td>Enabling caching greatly enhances load times. Before turning on caching, CHMOD the ronaldheft/feedburner/cache folder to 777.</td>
			</tr>
		</table>
HERE;
		$preferences['Cache Expiration Time'] = <<<HERE
		<table class='snug'>
			<tr>
				<td>Cache Expires in </td>
				<td><span class='inline'><input type='text' id='cachetime' size='3' maxlength='3' name='cachetime' value='{$prefs['cachetime']}' class='cinch' /></span></td>
				<td> Hours</td>
			</tr>
		</table>
HERE;
		}
		
		return $preferences;

	}
	
	/**************************************************************************
	 onSavePreferences()
	 **************************************************************************/
	function onSavePreferences() 
	{
		$this->prefs['feed'] = $this->escapeSQL($_POST['feed']);
		if ( isset($_POST['api']) )
			$this->prefs['api'] = $this->escapeSQL('https://feedburner.google.com/api/awareness/1.0/');
		else
			$this->prefs['api'] = $this->escapeSQL('http://api.feedburner.com/awareness/1.0/');
		$this->prefs['cache'] = (isset($_POST['cache']))?1:0;
		$this->prefs['cachetime'] = $this->escapeSQL($_POST['cachetime']);
	}
	
	/**************************************************************************
	onCustom()
	**************************************************************************/
	function onCustom() 
	{

	}
	
	/**************************************************************************
	get_Feed()
	**************************************************************************/
	function get_FeedData($url) 
	{
		// Prep cache
		$cache = $this->prefs['cache'];
		$cachetime = $this->prefs['cachetime'];
		$cachefile = dirname(__FILE__) . '/cache/' . md5($url) . '.cache';
		$cachetime = $cachetime * 3600;
		
		// Read from cache if possible
		if ($cache)
		{			  	
			if (file_exists($cachefile))
			{
				$cachefile_created = @filemtime($cachefile);
				@clearstatcache();
				
				if (time() - $cachetime < $cachefile_created)
					return unserialize(file_get_contents($cachefile));
			}
		}
		
		if(!function_exists('feedburner'))
			require_once 'class.feedburner.php';
		
		$feed =& new feedburner($url, $this->prefs['api']);
		$date_str = $this->Mint->offsetDate('Y-m-d', strtotime('-1 year -2 month')) . ',' . $this->Mint->offsetDate('Y-m-d');
		$info = $feed->getFeedData(array('dates'=>$date_str));
		$entries = $info['entries'];
	
		if ($feed->isError())
		{
			if ($feed->getErrorCode() == 2)
				$errorText = "Feedburner Awareness API is not enabled. Log into Feedburner to enable it.";
			else
				$errorText = $feed->getErrorMsg();
			
			return array ('','','',$errorText);
		} else {
			$months = array();
			$weeks = array();
			$days = array();
			
			// Crazy time conversions so strtotime can subtract months correctly
			$dayStart = strtotime($this->Mint->offsetDate('Y-m-d', strtotime('+12 hours', $this->Mint->getOffsetTime('today'))));
			$weekStart = strtotime($this->Mint->offsetDate('Y-m-d', strtotime('+12 hours', $this->Mint->getOffsetTime('week'))));
			$monthStart = strtotime($this->Mint->offsetDate('Y-m-d', strtotime('+12 hours', $this->Mint->getOffsetTime('month'))));
	
			// Adjust for slow Feedburner reporting
			$firstDay = array_reverse($entries);
			if ( strtotime($firstDay[0]['date']) < strtotime('-1 day', $dayStart) )
				$dayStart = strtotime('-1 day', $dayStart);
			if ( strtotime($firstDay[0]['date']) < $weekStart )
				$weekStart = strtotime('-1 week', $weekStart);
			if ( strtotime($firstDay[0]['date']) < monthStart )
				$monthStart = strtotime('-1 month', $monthStart);
	
			// Place days in correct time frame
			foreach ($entries as $entry)
			{
				// Convert to unix time
				$entry['date'] = strtotime($entry['date']);
	
				// Check for months
				if ( $entry['date'] >= strtotime('-11 month', $monthStart) )
				{
					if ( $entry['date'] < strtotime('-10 month', $monthStart) )
						$months[11][] = $entry;
					elseif ( $entry['date'] < strtotime('-9 month', $monthStart) )
						$months[10][] = $entry;
					elseif ( $entry['date'] < strtotime('-8 month', $monthStart) )
						$months[9][] = $entry;
					elseif ( $entry['date'] < strtotime('-7 month', $monthStart) )
						$months[8][] = $entry;
					elseif ( $entry['date'] < strtotime('-6 month', $monthStart) )
						$months[7][] = $entry;
					elseif ( $entry['date'] < strtotime('-5 month', $monthStart) )
						$months[6][] = $entry;
					elseif ( $entry['date'] < strtotime('-4 month', $monthStart) )
						$months[5][] = $entry;
					elseif ( $entry['date'] < strtotime('-3 month', $monthStart) )
						$months[4][] = $entry;
					elseif ( $entry['date'] < strtotime('-2 month', $monthStart) )
						$months[3][] = $entry;
					elseif ( $entry['date'] < strtotime('-1 month', $monthStart) )
						$months[2][] = $entry;
					elseif ( $entry['date'] < $monthStart )
						$months[1][] = $entry;
					else
						$months[0][] = $entry;
				}
		
				// Check for weeks
				if ( $entry['date'] >= strtotime('-4 week', $weekStart) )
				{
					if ( $entry['date'] < strtotime('-3 week', $weekStart) )
						$weeks[4][] = $entry;
					else if ( $entry['date'] < strtotime('-2 week', $weekStart) )
						$weeks[3][] = $entry;
					else if ( $entry['date'] < strtotime('-1 week', $weekStart) )
						$weeks[2][] = $entry;
					else if ( $entry['date'] < $weekStart )
						$weeks[1][] = $entry;
					else
						$weeks[0][] = $entry;
				}
		
				// Check for days
				if ( $entry['date'] >= strtotime('-7 days', $dayStart) )
				{
					$days[] = $entry;
				}
			}
	
			$avgMonths = array();
			$avgWeeks = array();
			
			$circulation = 0;
			$hits = 0;
			$count = 0;
	
			// Average weeks
			foreach ($months as $month)
			{				
				foreach ($month as $day)
				{
					$circulation = $circulation + $day['circulation'];
					$hits = $hits + $day['hits'];
					if ($day['hits'] != 0) $count++;
				}

				$avgMonths[] = array
				(
					'circulation' => round($circulation / $count),
					'hits' => round($hits / $count),
					'date' => $month[0]['date']
				);
				
				unset($circulation, $hits, $count);	
			}
			
			$circulation = 0;
			$hits = 0;
			$count = 0;
	
			// Average weeks
			foreach ($weeks as $week)
			{				
				foreach ($week as $day)
				{
					$circulation = $circulation + $day['circulation'];
					$hits = $hits + $day['hits'];
					if ($day['hits'] != 0) $count++;
				}
		
				$avgWeeks[] = array
				(
					'circulation' => round($circulation / $count),
					'hits' => round($hits / $count),
					'date' => $week[0]['date']
				);
				
				unset($circulation, $hits, $count);
			}
	
			// Reverse arrays for display
			$avgMonths = array_reverse($avgMonths);
			$avgWeeks = array_reverse($avgWeeks);
			$days = array_reverse($days);
			
			$feedData = array($days, $avgWeeks, $avgMonths, '');
			
			// Write cache information
			if ($cache)
			{
				$file_exists = file_exists($cachefile);
			   	$myfile = fopen($cachefile, "w");
				fwrite($myfile, serialize($feedData));
				if (is_resource($myfile && $file_exists))
					fclose($myfile);
			}
	
			return $feedData;
		}
	}
	
	/**************************************************************************
	 getHTML_Overview()
	 **************************************************************************/
	function getHTML_Overview()		
	{		
		$html = '';
		$error = false;
		$wcount = 0;
		$mcount = 0;
		
		$filters = array();
		$data = array();
		$avgMonths = array();
		$avgWeeks = array();
		$days = array();
		
		$urls = explode(',', $this->prefs['feed']);
		
		foreach ($urls as $url)
		{
			$url = trim($url);
			$filters[$url] = $url;
		}

		if ( $this->prefs['feed'] != '' ) 
		{
			// Generate filters
			if ( count($filters) != 1)
				$filterlist = $this->generateFilterList('Overview', $filters);

			// If currently selected on old url
			if ( !in_array($this->filter, $filters, true) )
				$this->filter = $url;
			
			$data = $this->get_FeedData($this->filter);
			$days = $data[0];
			$avgWeeks = $data[1];
			$avgMonths = $data[2];
			
			if ($data[3])
			{
				$error = true;
				$errorText = $data[3];
			}
			
			$tableData['table'] = array('id'=>'','class'=>'inline-foot striped');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>'Past Week','class'=>'focus'),
				array('value'=>'<abbr title="Total Subscribers">Scribs</abbr>','class'=>''),
				array('value'=>'<abbr title="Total Hits">Hits</abbr>','class'=>'')			
			);

			foreach ($days as $day) 
			{
				$date = date("l", $day['date']);
				
				if ($day['circulation'] == 0) $day['circulation'] = "-";
				if ($day['hits'] == 0) $day['hits'] = "-";
				
				$tableData['tbody'][] = array
				(
					$date,
					$day['circulation'],
					$day['hits']
				);
			}
			
			$weekHTML = $this->Mint->generateTable($tableData);
			unset($tableData);
			
			$tableData['table'] = array('id'=>'','class'=>'inline inline-foot striped');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>'Past Month','class'=>'focus'),
				array('value'=>'<abbr title="Average Subscribers">Scribs</abbr>','class'=>''),
				array('value'=>'<abbr title="Average Hits">Hits</abbr>','class'=>'')			
			);

			foreach ($avgWeeks as $avgWeek) 
			{
				if ($wcount == 0) $date = "This Week";
				elseif ($wcount == 1) $date = "Last Week";
				else $date = $wcount . " weeks ago";
				
				if ($avgWeek['circulation'] == 0) $avgWeek['circulation'] = "-";
				if ($avgWeek['hits'] == 0) $avgWeek['hits'] = "-";
				
				$tableData['tbody'][] = array
				(
					$date,
					$avgWeek['circulation'],
					$avgWeek['hits']
				);
				
				$wcount++;
			}
			
			$monthHTML = $this->Mint->generateTable($tableData);
			unset($tableData);
			
			$tableData['table'] = array('id'=>'','class'=>'inline year striped');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>'Past Year','class'=>'focus'),
				array('value'=>'<abbr title="Average Subscribers">Scribs</abbr>','class'=>''),
				array('value'=>'<abbr title="Average Hits">Hits</abbr>','class'=>'')
			);

			foreach ($avgMonths as $avgMonth) 
			{
				$date = date("M 'y", $avgMonth['date']);
				if ($mcount == 0) $date = "This Month";
				
				if ($avgMonth['circulation'] == 0) $avgMonth['circulation'] = "-";
				if ($avgMonth['hits'] == 0) $avgMonth['hits'] = "-";
				
				$tableData['tbody'][] = array
				(
					$date,
					$avgMonth['circulation'],
					$avgMonth['hits']
				);
				
				$mcount++;
			}
			
			$yearHTML = $this->Mint->generateTable($tableData);
			unset($tableData);
			
			$html	.= '<table cellspacing="0" class="visits">';
			$html	.= "\r\t<tr>\r";
			$html	.= "\t\t<td class=\"left\">\r";
			$html	.= $weekHTML.$monthHTML;
			$html	.= "\t\t</td>";
			$html	.= "\t\t<td class=\"right\">\r";
			$html	.= $yearHTML;
			$html	.= "\t\t</td>";
			$html	.= "\r\t</tr>\r";
			$html	.= "</table>\r";
			
		} else {
			$error = true;
			$errorText = "Feedburner URL not configured.";
		}
		
		if ($error)
		{
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>"Error Getting Feed Report",'class'=>'focus')		
			);
			$tableData['tbody'][] = array
			(
				'<strong>Error</strong>: '.$errorText
			);
			$html = $this->Mint->generateTable($tableData);
		}
		
		return $filterlist . $html;
	}
	
	
	/**************************************************************************
	 getHTML_Week()
	 **************************************************************************/
	function getHTML_Week()		
	{		
		$html = '';
		$high = 0;
		
		$filters = array();
		$data = array();
		$days = array();
		
		$urls = explode(',', $this->prefs['feed']);
		
		foreach ($urls as $url)
		{
			$url = trim($url);
			$filters[$url] = $url;
		}
		
		if ( $this->prefs['feed'] != '' ) 
		{
			// Generate filters
			if ( count($filters) != 1)
				$filterlist = $this->generateFilterList('Past Week', $filters);

			// If currently selected on old url
			if ( !in_array($this->filter, $filters, true) )
				$this->filter = $url;
		
			$data = $this->get_FeedData($this->filter);
			$days = $data[0];
			
			if ($data[3])
			{
				$error = true;
				$cache = false;
				$errorText = $data[3];
			}
		
			$graphData	= array
			(
				'titles' => array
				(
					'background' => 'Hits',
					'foreground' => 'Subscribers'
				),
				'key' => array
				(
					'background' => 'Hits',
					'foreground' => 'Scribs'
				)
			);
		
			foreach ($days as $day) 
			{
				$high = ($day['hits'] > $high) ? $day['hits'] : $high;
				
				$dayOfWeek = date('w', $day['date']);
				$dayLabel = substr(date('D', $day['date']), 0, 2);
			
				$graphData['bars'][] = array
				(
					$day['hits'],
					$day['circulation'],
					($dayOfWeek == 0) ? '' : (($dayOfWeek == 6) ? 'Weekend' : $dayLabel),
					date('l', $day['date']),
					($dayOfWeek == 0 || $dayOfWeek == 6) ? 1 : 0
				);
			}
		
			$graphData['bars'] = array_reverse($graphData['bars']);
			$html .= $this->getHTML_Graph($high, $graphData);
		
		} else {
			$error = true;
			$errorText = "Feedburner URL not configured.";
		}
		
		if ($error)
		{
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>"Error Getting Feed Report",'class'=>'focus')		
			);
			$tableData['tbody'][] = array
			(
				'<strong>Error</strong>: '.$errorText
			);
			$html = $this->Mint->generateTable($tableData);
		}
		
		return $filterlist . $html;
	}
	
	
	/**************************************************************************
	 getHTML_Month()
	 **************************************************************************/
	function getHTML_Month()		
	{		
		$html = '';
		$high = 0;
		
		$filters = array();
		$data = array();
		$weeks = array();
		
		$urls = explode(',', $this->prefs['feed']);
		
		foreach ($urls as $url)
		{
			$url = trim($url);
			$filters[$url] = $url;
		}
		
		if ( $this->prefs['feed'] != '' ) 
		{
			// Generate filters
			if ( count($filters) != 1)
				$filterlist = $this->generateFilterList('Past Month', $filters);

			// If currently selected on old url
			if ( !in_array($this->filter, $filters, true) )
				$this->filter = $url;
		
			$data = $this->get_FeedData($this->filter);
			$weeks = $data[1];
			
			if ($data[3])
			{
				$error = true;
				$cache = false;
				$errorText = $data[3];
			}
		
			$graphData	= array
			(
				'titles' => array
				(
					'background' => 'Average Hits',
					'foreground' => 'Average Subscribers'
				),
				'key' => array
				(
					'background' => 'Hits',
					'foreground' => 'Scribs'
				)
			);
		
			foreach ($weeks as $week) 
			{
				$high = ($week['hits'] > $high) ? $week['hits'] : $high;
			
				$graphData['bars'][] = array
				(
					$week['hits'],
					$week['circulation'],
					$this->Mint->formatDateRelative($week['date'], "week", $i),
					date('D, M j', $week['date']),
					($i == 0) ? 1 : 0
				);
				
				$i++;
			}
		
			$graphData['bars'] = array_reverse($graphData['bars']);
			$html .= $this->getHTML_Graph($high, $graphData);
		
		} else {
			$error = true;
			$errorText = "Feedburner URL not configured.";
		}
		
		if ($error)
		{
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>"Error Getting Feed Report",'class'=>'focus')		
			);
			$tableData['tbody'][] = array
			(
				'<strong>Error</strong>: '.$errorText
			);
			$html = $this->Mint->generateTable($tableData);
		}
		
		return $filterlist . $html;
	}
	
	
	/**************************************************************************
	 getHTML_Year()
	 **************************************************************************/
	function getHTML_Year()		
	{		
		$html = '';
		$high = 0;
		
		$filters = array();
		$data = array();
		$months = array();
		
		$urls = explode(',', $this->prefs['feed']);
		
		foreach ($urls as $url)
		{
			$url = trim($url);
			$filters[$url] = $url;
		}
		
		if ( $this->prefs['feed'] != '' ) 
		{
			// Generate filters
			if ( count($filters) != 1)
				$filterlist = $this->generateFilterList('Past Year', $filters);

			// If currently selected on old url
			if ( !in_array($this->filter, $filters, true) )
				$this->filter = $url;
		
			$data = $this->get_FeedData($this->filter);
			$months = $data[2];
			
			if ($data[3])
			{
				$error = true;
				$cache = false;
				$errorText = $data[3];
			}
		
			$graphData	= array
			(
				'titles' => array
				(
					'background' => 'Average Hits',
					'foreground' => 'Average Subscribers'
				),
				'key' => array
				(
					'background' => 'Hits',
					'foreground' => 'Scribs'
				)
			);
		
			foreach ($months as $month) 
			{
				$high = ($month['hits'] > $high) ? $month['hits'] : $high;
			
				$graphData['bars'][] = array
				(
					$month['hits'],
					$month['circulation'],
					($i == 0) ? 'This Month' : date(' M', $month['date']),
					date('F', $month['date']),
					($i == 0) ? 1 : 0
				);
				
				$i++;
			}
		
			$graphData['bars'] = array_reverse($graphData['bars']);
			$html .= $this->getHTML_Graph($high, $graphData);
		
		} else {
			$error = true;
			$errorText = "Feedburner URL not configured.";
		}
		
		if ($error)
		{
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>"Error Getting Feed Report",'class'=>'focus')		
			);
			$tableData['tbody'][] = array
			(
				'<strong>Error</strong>: '.$errorText
			);
			$html = $this->Mint->generateTable($tableData);
		}
		
		return $filterlist . $html;
	}
	
	
	/**************************************************************************
	get_ItemData()
	**************************************************************************/
	function get_ItemData($url, $date) 
	{
		// Prep cache
		$cache = $this->prefs['cache'];
		$cachetime = $this->prefs['cachetime'];
		$cachefile = dirname(__FILE__) . '/cache/' . md5($url) . '.itemcache';
		$cachetime = $cachetime * 3600;
		
		// Read from cache if possible
		if ($cache)
		{			  	
			if (file_exists($cachefile))
			{
				$cachefile_created = @filemtime($cachefile);
				@clearstatcache();
				
				if (time() - $cachetime < $cachefile_created)
					return unserialize(file_get_contents($cachefile));
			}
		}
		
		if(!function_exists('feedburner'))
			require_once 'class.feedburner.php';
			
		$feed =& new feedburner($url, $this->prefs['api']);
		$date_str = $this->Mint->offsetDate('Y-m-d', strtotime('-2 day'));
		$info = ($date) ? $feed->getItemData(array('dates'=>$date_str)) : $feed->getItemData();
		$entries = $info['entries'][1]['items'];
	
		if ($feed->isError())
		{
			if ($feed->getErrorCode() == 2)
				$errorText = "Feedburner Awareness API is not enabled. Log into Feedburner to enable it.";
			elseif ($feed->getErrorCode() == 4)
				$errorText = "Item tracking is not enabled. Log into Feedburner to enable it.";
			else
				$errorText = $feed->getErrorMsg();
			
			return array ('',$errorText);
		} else {
			$itemData = array();
			
			if (count($entries) > 0) {
				foreach ($entries as $entry) {
					$itemData[] = array(
						'url' => $entry['url'],
						'title' => $entry['title'],
						'hits' => $entry['itemviews'],
						'clicks' => $entry['clickthroughs']
					);
					$numItems++;
					if ($numItems >= $this->Mint->cfg['preferences']['rows'])
						break;
				}
			} else {
				if (!$date)
					return $this->get_ItemData($url, true);
				$errorText = "No item statistics. If you just enabled item tracking, wait a day for statistics to appear.";
				return array ('',$errorText);
			}
			
			$feedData = array($itemData, '');
			
			// Write cache information
			if ($cache)
			{
				$file_exists = file_exists($cachefile);
			   	$myfile = fopen($cachefile, "w");
				fwrite($myfile, serialize($feedData));
				if (is_resource($myfile && $file_exists))
					fclose($myfile);
			}
	
			return $feedData;
		}
	}
	
	
	/**************************************************************************
	 getHTML_Items()
	 **************************************************************************/
	function getHTML_Items()		
	{		
		$html = '';
		$error = false;
		
		$filters = array();
		$data = array();
		
		$urls = explode(',', $this->prefs['feed']);
		
		foreach ($urls as $url)
		{
			$url = trim($url);
			$filters[$url] = $url;
		}

		if ( $this->prefs['feed'] != '' ) 
		{
			// Generate filters
			if ( count($filters) != 1)
				$filterlist = $this->generateFilterList('Refresh', $filters);

			// If currently selected on old url
			if ( !in_array($this->filter, $filters, true) )
				$this->filter = $url;
			
			$data = $this->get_ItemData($this->filter);
			
			if ($data[1])
			{
				$error = true;
				$errorText = $data[1];
			}
			
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>'Clicks','class'=>'sort'),
				array('value'=>'Feed Item','class'=>'focus'),
				array('value'=>'Views','class'=>'sort')			
			);

			foreach ($data[0] as $item) 
			{				
				$tableData['tbody'][] = array
				(
					$item['clicks'],
					'<a href="' . $item['url'] .'">' . $this->convert_encoding($item['title']) . '</a>',
					$item['hits']
				);
			}
			
			$html = $this->Mint->generateTable($tableData);
			
		} else {
			$error = true;
			$errorText = "Feedburner URL not configured.";
		}
		
		if ($error)
		{
			$tableData['table'] = array('id'=>'','class'=>'');
			$tableData['thead'] = array
			(
				// display name, CSS class(es) for each column
				array('value'=>"Error Getting Feed Report",'class'=>'focus')		
			);
			$tableData['tbody'][] = array
			(
				'<strong>Error</strong>: '.$errorText
			);
			$html = $this->Mint->generateTable($tableData);
		}
		
		return $filterlist . $html;
	}
	
	
	/**************************************************************************
	 convert_encoding()
	 **************************************************************************/
	function convert_encoding($string)
	{
		$search = array(chr(0xe2) . chr(0x80) . chr(0x98),
			chr(0xe2) . chr(0x80) . chr(0x99),
			chr(0xe2) . chr(0x80) . chr(0x9c),
			chr(0xe2) . chr(0x80) . chr(0x9d),
			chr(0xe2) . chr(0x80) . chr(0x93),
			chr(0xe2) . chr(0x80) . chr(0x94));

		$replace = array('&lsquo;',
			'&rsquo;',
			'&ldquo;',
			'&rdquo;',
			'&ndash;',
			'&mdash;');

		return str_replace($search, $replace, $string);
	}
	
}