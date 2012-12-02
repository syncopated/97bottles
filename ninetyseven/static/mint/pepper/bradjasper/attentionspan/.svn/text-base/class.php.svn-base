<?php
/******************************************************************************
 Pepper

 Developer      : Brad Jasper
 Plug-in Name   : Attention Span

 [bradjasper.com](http://www.bradjasper.com/)

 ******************************************************************************/
 if (!defined('MINT')) { header('Location:/'); }; // Prevent viewing this file directly

$installPepper = "BJ_AttentionSpan";

class BJ_AttentionSpan extends Pepper
{
	var $version    = 3; // Displays as 0.01
	var $info       = array
	(
		'pepperName'    => 'Attention Span',
		'pepperUrl'     => 'http://www.bradjasper.com/',
		'pepperDesc'    => 'Attention span shows how long your visitors stick around by dislaying bounce rates and pages per visit information. The higher the pages per visit and lower the bounce rate the "stickier" your content.',
		'developerName' => 'Brad Jasper',
		'developerUrl'  => 'http://www.bradjasper.com/'
	);
	var $panes = array
	(
		'Attention Span' => array
		(
			'Quick View',
			'Bounce Rates',
			'Pages Per Visit'
		)
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
				'isCompatible'  => true
			);
		}
		else
		{
			return array
			(
				'isCompatible'  => false,
				'explanation'   => '<p>This Pepper is only compatible with Mint 1.2 and higher.</p>'
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
			/* Attention Span ***************************************************/
			case 'Attention Span': 
				switch($tab)
				{
					/* Overview ************************************************/
					case 'Quick View':
						$html .= $this->getHTML_QuickLook();
						break;
					/* Bounce Rates ************************************************/
					case 'Bounce Rates':
						$html .= $this->getHTML_BounceRates();
						break;
					/* Pages Per Visit ************************************************/
					case 'Pages Per Visit':
						$html .= $this->getHTML_PagesPerVisit();
						break;
				}
				break;
		}
		return $html;
	}

	/**************************************************************************
	 getHTML_QuickLook()
	 **************************************************************************/
	function getHTML_QuickLook() {
		
		//	Let's set the data we're going to be using
		$days		= $this->Mint->data[0]['visits'][2];
		$day		= $this->Mint->getOffsetTime('today');
		
		$weeks		= $this->Mint->data[0]['visits'][3];
		$week 		= $this->Mint->getOffsetTime('week');
		
		$months		= $this->Mint->data[0]['visits'][4];
		$month 		= $this->Mint->getOffsetTime('month');


		//	Bounce Rates Quicklook
		$tableData['table'] = array('id'=>'','class'=>'inline year striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Time Period','class'=>'focus'),
			array('value'=>'Bounce Rate','class'=>''),
			array('value'=>'Pages Per Visit','class'=>'')
		);
		$tableData['tbody'][] = array
		(
			'Past Day',
			$this->getBouncePages('bouncerate', $days[$day]['total'], $days[$day]['unique'], 1),
			$this->getBouncePages('pagespervisit', $days[$day]['total'], $days[$day]['unique'])
		);
		$tableData['tbody'][] = array
		(
			'Past Week',
			$this->getBouncePages('bouncerate', $weeks[$week]['total'], $weeks[$week]['unique'], 1),
			$this->getBouncePages('pagespervisit', $weeks[$week]['total'], $weeks[$week]['unique'])
		);
		$tableData['tbody'][] = array
		(
			'Past Month',
			$this->getBouncePages('bouncerate', $months[$month]['total'], $months[$month]['unique'], 1),
			$this->getBouncePages('pagespervisit', $months[$month]['total'], $months[$month]['unique'])
		);
		

		$quickLookHTML = $this->Mint->generateTable($tableData);
		
		$quickLookHTML = '<table class="visits" cellspacing="0">
							<tr>
								<td class="right">
									' . $quickLookHTML . '
								</td>
							</tr>
						</table>';
		
		return $quickLookHTML;

	}

	/**************************************************************************
	 getHTML_BounceRates()
	 **************************************************************************/
	 function getHTML_BounceRates() {

		$filters = array
		(
			'Overview'	=> 0,
			'Past Day'	=> 1,
			'Week'		=> 2,
			'Month'		=> 3,
			'Year'		=> 4,

		);
		$html .= $this->generateFilterList('Bounce Rates', $filters, $this->panes['Attention Span']);

		switch ($this->filter) {
			case 0:
				$html .= $this->getHTML_Overview('bouncerate');
				break;
			case 1:
				$html .= $this->getHTML_PastDay('bouncerate');
				break;
			case 2:
				$html .= $this->getHTML_PastWeek('bouncerate');
				break;
			case 3:
				$html .= $this->getHTML_PastMonth('bouncerate');
				break;
			case 4:
				$html .= $this->getHTML_PastYear('bouncerate');
				break;
		}

		return $html;

	 }

	/**************************************************************************
	 getHTML_PagesPerVisit()
	 **************************************************************************/
	 function getHTML_PagesPerVisit() {

		$filters = array
		(
			'Overview'	=> 0,
			'Past Day'	=> 1,
			'Week'		=> 2,
			'Month'		=> 3,
			'Year'		=> 4,

		);
		$html .= $this->generateFilterList('Pages Per Visit', $filters, $this->panes['Attention Span']);

		switch ($this->filter) {
			case 0:
				$html .= $this->getHTML_Overview('pagespervisit');
				break;
			case 1:
				$html .= $this->getHTML_PastDay('pagespervisit');
				break;
			case 2:
				$html .= $this->getHTML_PastWeek('pagespervisit');
				break;
			case 3:
				$html .= $this->getHTML_PastMonth('pagespervisit');
				break;
			case 4:
				$html .= $this->getHTML_PastYear('pagespervisit');
				break;
		}

		return $html;

	 }

	/**************************************************************************
	 getHTML_PastDay()
	 **************************************************************************/
	function getHTML_PastDay($type) 
	{
		$high 		= 0;
		$hours		= $this->Mint->data[0]['visits'][1];
		$hour 		= $this->Mint->getOffsetTime('hour');

		// Past 24 hours
		for ($i = 0; $i < 24; $i++) 
		{
			$timestamp = $hour - ($i * 60 * 60);
			$counts = array(0, 0);
			if (isset($hours[$timestamp]))
			{
				$counts = array($hours[$timestamp]['total'], $hours[$timestamp]['unique']);
			}
			
			$twelve = $this->Mint->offsetDate('G', $timestamp) == 12;
			$twentyFour = $this->Mint->offsetDate('G', $timestamp) == 0;
			$hourLabel = $this->Mint->offsetDate('g', $timestamp);

			if ($type == 'bouncerate') {
				$bounce_rate = round(($counts[1] / $counts[0]) * 100);
				$high = ($bounce_rate > $high) ? $bounce_rate : $high;

			} else if ($type == 'pagespervisit') {
				$pages_per_visit = round(($counts[0] / $counts[1]), 1);
				$high = ($pages_per_visit > $high) ? $pages_per_visit : $high;
			}
			
			$graphData['bars'][] = array
			(
				($type == 'bouncerate' ? $bounce_rate : $pages_per_visit),
				'',
				($twelve) ? 'Noon' : (($twentyFour) ? 'Midnight' : (($hourLabel == 3 || $hourLabel == 6 || $hourLabel == 9) ? $hourLabel : '')),
				$this->Mint->formatDateRelative($timestamp, "hour"),
				($twelve || $twentyFour) ? 1 : 0
			);
		}
		
		$graphData['bars'] = array_reverse($graphData['bars']);
		$html = $this->getHTML_Graph(ceil($high), $graphData, $type);
		return $html;
	}

	/**************************************************************************
	 getHTML_PastWeek()
	 **************************************************************************/
	function getHTML_PastWeek($type) 
	{
		$high 		= 0;
		$days		= $this->Mint->data[0]['visits'][2];
		$day		= $this->Mint->getOffsetTime('today');

		// Past 7 days
		for ($i = 0; $i < 7; $i++) 
		{
			$timestamp = $day - ($i * 60 * 60 * 24);
			$counts = array(0, 0);
			if (isset($days[$timestamp]))
			{
				$counts = array($days[$timestamp]['total'], $days[$timestamp]['unique']);
			}
			
			$dayOfWeek = $this->Mint->offsetDate('w', $timestamp);
			$dayLabel = substr($this->Mint->offsetDate('D', $timestamp), 0, 2);

			if ($type == 'bouncerate') {
				$bounce_rate = round(($counts[1] / $counts[0]) * 100);
				$high = ($bounce_rate > $high) ? $bounce_rate : $high;

			} else if ($type == 'pagespervisit') {
				$pages_per_visit = round(($counts[0] / $counts[1]), 1);
				$high = ($pages_per_visit > $high) ? $pages_per_visit : $high;
			}

			$graphData['bars'][] = array
			(
				($type == 'bouncerate' ? $bounce_rate : $pages_per_visit),
				'',
				($dayOfWeek == 0) ? '' : (($dayOfWeek == 6) ? 'Weekend' : $dayLabel),
				$this->Mint->formatDateRelative($timestamp, "day"),
				($dayOfWeek == 0 || $dayOfWeek == 6) ? 1 : 0
			);
		}

		$graphData['bars'] = array_reverse($graphData['bars']);
		$html = $this->getHTML_Graph(ceil($high), $graphData, $type);

		return $html;
	}

	/**************************************************************************
	 getHTML_PastMonth()
	 **************************************************************************/
	function getHTML_PastMonth($type) 
	{

		$high 		= 0;
		$weeks		= $this->Mint->data[0]['visits'][3];
		$week 		= $this->Mint->getOffsetTime('week');
		
		// Past 5 weeks
		for ($i = 0; $i < 5; $i++)
		{
			$timestamp = $week - ($i * 60 * 60 * 24 * 7);
			$counts = array(0, 0);
			if (isset($weeks[$timestamp]))
			{
				$counts = array($weeks[$timestamp]['total'], $weeks[$timestamp]['unique']);
			}
			
			if ($type == 'bouncerate') {
				$bounce_rate = round(($counts[1] / $counts[0]) * 100);
				$high = ($bounce_rate > $high) ? $bounce_rate : $high;
			} else if ($type == 'pagespervisit') {
				$pages_per_visit = round($counts[0] / $counts[1], 1);
				$high = ($pages_per_visit > $high) ? $pages_per_visit : $high;
			}

			
			$graphData['bars'][] = array
			(
				($type == 'bouncerate' ? $bounce_rate : $pages_per_visit),
				'',
				$this->Mint->formatDateRelative($timestamp, "week", $i),
				$this->Mint->offsetDate('D, M j', $timestamp),
				($i == 0) ? 1 : 0
			);
		}
		
		$graphData['bars'] = array_reverse($graphData['bars']);
		$html = $this->getHTML_Graph(ceil($high), $graphData, $type);
		return $html;
	}

	/**************************************************************************
	 getHTML_PastYear()
	 **************************************************************************/
	function getHTML_PastYear($type) 
	{
		$high 		= 0;
		$months		= $this->Mint->data[0]['visits'][4];
		$month 		= $this->Mint->getOffsetTime('month');
		
		// Past 12 months
		for ($i = 0; $i < 12; $i++)
		{
			if ($i == 0)
			{
				$timestamp = $month;
			}
			else
			{
				$days 		= $this->Mint->offsetDate('t', $this->Mint->offsetMakeGMT(0, 0, 0, $this->Mint->offsetDate('n', $month)-1, 1, $this->Mint->offsetDate('Y', $month))); // days in the month
				$timestamp 	= $month - ($days * 24 * 3600);
			}
			$month = $timestamp;
			
			$counts = array(0, 0);
			if (isset($months[$timestamp]))
			{
				$counts = array($months[$timestamp]['total'], $months[$timestamp]['unique']);
			}
				
			if ($type == 'bouncerate') {
				$bounce_rate = round(($counts[1] / $counts[0]) * 100);
				$high = ($bounce_rate > $high) ? $bounce_rate : $high;
			} else if ($type == 'pagespervisit') {
				$pages_per_visit = round($counts[0] / $counts[1], 1);
				$high = ($pages_per_visit > $high) ? $pages_per_visit : $high;
			}
			
			$graphData['bars'][] = array
			(
				($type == 'bouncerate' ? $bounce_rate : $pages_per_visit),
				'',
				($i == 0) ? 'This Month' : $this->Mint->offsetDate(' M', $timestamp),
				$this->Mint->offsetDate('F', $timestamp),
				($i == 0) ? 1 : 0
			);
		}
		
		$graphData['bars'] = array_reverse($graphData['bars']);
		$html = $this->getHTML_Graph(ceil($high), $graphData, $type);
		return $html;
	}

	/**************************************************************************
	 getHTML_Overview()
	 **************************************************************************/
	function getHTML_Overview($type) 
	{
		$visits	= $this->Mint->data[0]['visits'];

		$sHeader = ($type == "bouncerate" ? "Bounce Rate" : "Pages Per Visit");
		
		/* Since **************************************************************/
		$tableData['table'] = array('id'=>'','class'=>'inline-foot striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Since','class'=>'focus'),
			array('value'=>'<abbr title="' . $sHeader . '">' . $sHeader . '</abbr>','class'=>'')
		);

		$tableData['tbody'][] = array
		(
			$this->Mint->formatDateRelative($this->Mint->cfg['installDate'], 'month', 1),
			$this->getBouncePages($type, $visits[0][0]['total'], $visits[0][0]['unique'], 1)
		);
		$sinceHTML = $this->Mint->generateTable($tableData);
		unset($tableData);
		
		
		/* Past Day ***********************************************************/
		$tableData['table'] = array('id'=>'','class'=>'inline day striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Past Day','class'=>'focus'),
			array('value'=>'<abbr title="' . $sHeader . '">' . $sHeader . '</abbr>','class'=>'')
		);
		$hour = $this->Mint->getOffsetTime('hour');
		// Past 24 hours
		for ($i=0; $i<24; $i++) 
		{
			$j = $hour - ($i*60*60);
			if (isset($visits[1][$j]))
			{
				$h = $visits[1][$j];
			}
			else
			{
				$h = array('total'=>'-','unique'=>'-');
			}
			$tableData['tbody'][] = array
			(
				$this->Mint->formatDateRelative($j,"hour"),
				$this->getBouncePages($type, $h['total'], $h['unique'], 1)
			);
		}
		$dayHTML = $this->Mint->generateTable($tableData);
		unset($tableData);
		

		/* Past Week **********************************************************/
		$tableData['table'] = array('id'=>'','class'=>'inline-foot striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Past Week','class'=>'focus'),
			array('value'=>'<abbr title="' . $sHeader . '">' . $sHeader . '</abbr>','class'=>'')
		);
		$day = $this->Mint->getOffsetTime('today');
		// Past 7 days
		for ($i=0; $i<7; $i++) 
		{
			$j = $day - ($i*60*60*24);
			if (isset($visits[2][$j]))
			{
				$d = $visits[2][$j];
			}
			else
			{
				$d = array('total'=>'-','unique'=>'-');
			}
			$tableData['tbody'][] = array
			(
				$this->Mint->formatDateRelative($j,"day"),
				$this->getBouncePages($type, $d['total'], $d['unique'], 1)
			);
		}
		$weekHTML = $this->Mint->generateTable($tableData);
		unset($tableData);
		
		
		/* Past Month *********************************************************/
		$tableData['table'] = array('id'=>'','class'=>'inline inline-foot striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Past Month','class'=>'focus'),
			array('value'=>'<abbr title="' . $sHeader . '">' . $sHeader .'</abbr>','class'=>'')
		);
		$week = $this->Mint->getOffsetTime('week');
		// Past 5 weeks
		for ($i=0; $i<5; $i++)
		{
			$j = $week - ($i*60*60*24*7);
			if (isset($visits[3][$j]))
			{
				$w = $visits[3][$j];
			}
			else
			{
				$w = array('total'=>'-','unique'=>'-');
			}
			$tableData['tbody'][] = array
			(
				$this->Mint->formatDateRelative($j,"week",$i),
				$this->getBouncePages($type, $w['total'], $w['unique'], 1)
			);
		}
		$monthHTML = $this->Mint->generateTable($tableData);
		unset($tableData);
		
		
		/* Past Year **********************************************************/
		$tableData['table'] = array('id'=>'','class'=>'inline year striped');
		$tableData['thead'] = array
		(
			// display name, CSS class(es) for each column
			array('value'=>'Past Year','class'=>'focus'),
			array('value'=>'<abbr title="' . $sHeader . '">' . $sHeader . '</abbr>','class'=>'')
		);
		$month = $this->Mint->getOffsetTime('month');
		$totalUnique = 0;
		$totalVisits = 0;
		// Past 12 months
		for ($i=0; $i<12; $i++)
		{
			if ($i==0)
			{
				$j=$month;
			}
			else
			{
				$days 		= $this->Mint->offsetDate('t', $this->Mint->offsetMakeGMT(0, 0, 0, $this->Mint->offsetDate('n', $month)-1, 1, $this->Mint->offsetDate('Y', $month))); // days in the month
				$j 			= $month - ($days*24*3600);
			}
			
			$month = $j;
			if (isset($visits[4][$j]))
			{
				$m = $visits[4][$j];
			}
			else
			{
				$m = array('total'=>'-','unique'=>'-');
			}

			$tableData['tbody'][] = array
			(
				$this->Mint->formatDateRelative($j, 'month', $i),
				$this->getBouncePages($type, $m['total'], $m['unique'], 1)
			);
		}

		$yearHTML = $this->Mint->generateTable($tableData);
		unset($tableData);
		
		/**/
		$html  = '<table cellspacing="0" class="visits">';
		$html .= "\r\t<tr>\r";
		$html .= "\t\t<td class=\"left\">\r";
		$html .= $sinceHTML.$dayHTML;
		$html .= "\t\t</td>";
		$html .= "\t\t<td class=\"right\">\r";
		$html .= $weekHTML.$monthHTML.$yearHTML;
		$html .= "\t\t</td>";
		$html .= "\r\t</tr>\r";
		$html .= "</table>\r";
		return $html;
	}

	function getBouncePages($type, $total, $unique, $format = 0) {
		if ($type == 'bouncerate') {
			return round(($unique / $total) * 100) . ($format ? "%" : "");
		} else if ($type == 'pagespervisit') {
			return round($total / $unique, 1);
		}
	}


}