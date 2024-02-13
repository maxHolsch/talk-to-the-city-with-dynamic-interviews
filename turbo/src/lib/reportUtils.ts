import _ from 'lodash';
import { findAncestor } from '$lib/hierarchy';
import { scaleOrdinal } from 'd3-scale';
import { hsl } from 'd3-color';

const customColors = [
	'#125761',
	'#D67A0A',
	'#0073D1',
	'#A72E16',
	'#6A9217',
	'#004C9E',
	'#704A01',
	'#70398A',
	'#00808A',
	'#B85914',
	'#3F2A7E',
	'#A94481',
	'#6169B3'
];

export const ordinalColor = scaleOrdinal(customColors);

export function getNodeColor(node: any) {
	const colorParent = findAncestor(node, (n) => n.depth === 1);
	return colorParent ? hsl(ordinalColor(colorParent.data.name)).brighter(node.depth * 0.3) : '#ddd';
}

export function scrollToTopic(topicName) {
	console.log(topicName);
	const mainContent = document.getElementById('report-main');
	if (mainContent) {
		const targetId = _.kebabCase('report-' + topicName);
		console.log(targetId);
		const targetElement = mainContent.querySelector(`#${targetId}`);
		console.log(targetElement);
		if (targetElement) {
			var rect = targetElement.getBoundingClientRect();
			var scrollTop = mainContent.scrollTop;
			var absoluteYPos = rect.top + scrollTop - 50;
			mainContent.scroll({
				top: absoluteYPos,
				left: 0,
				behavior: 'smooth'
			});
		}
	}
}