/**
 * Created with JetBrains PhpStorm.
 * User: lbedford
 * Date: 14.08.13
 * Time: 09:04
 * To change this template use File | Settings | File Templates.
 */
function ToggleDisplay(element_id) {
    var element = document.getElementById(element_id);
    if (!element) {
        window.alert('Failed to find ' + element_id);
    }
    if (element.style.visibility == 'visible') {
        element.style.visibility = 'hidden';
    } else {
        element.style.visibility = 'visible';
    }
}