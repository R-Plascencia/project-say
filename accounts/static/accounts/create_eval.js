window.onload = function(){
  //get elements
  var titleselect = document.getElementById('title');
  var keywords = document.getElementById('keywords');
  var invalid_title = false;

  titleselect.oninput = function(){
    // The title field is blank
   if( this.value == '' ){
     invalid_title = true;
     document.getElementById('title_div').className = 'form-group has-error';
     document.getElementById('errormessage').innerHTML = 'Whoops! Interest must have a title!';
    //  document.getElementById('createbutton').className = 'btn btn-primary btn-success btn-lg btn-block disabled';
     $('#createbutton').prop('disabled', true);
   } else { // Return the title field back to normal
      invalid_title = false;
      document.getElementById('title_div').className = 'form-group';
      document.getElementById('errormessage').innerHTML = '';
      // document.getElementById('createbutton').className = 'btn btn-primary btn-success btn-lg btn-block';
      $('#createbutton').prop('disabled', false);
    }
  };

  //input changed event
  keywords.oninput = function(){
    // If keyword field is blank
    // if(this.value == ''){
    //   $('#createbutton').prop('disabled', true);
    // }

    // There's more than 4 keywords entered
    if(this.value.split(',').length > 4){
      document.getElementById('keywords_div').className = 'form-group has-error';
      document.getElementById('errormessage').innerHTML = 'Whoops! Interest can\'t have more than 4 comma-separated keywords!';
      // document.getElementById('createbutton').className = 'btn btn-primary btn-success btn-lg btn-block disabled';
      $('#createbutton').prop('disabled', true);
    } else { //Return the keyword field back to normal
       if(! invalid_title){
         document.getElementById('keywords_div').className = 'form-group';
         document.getElementById('errormessage').innerHTML = '';
        //  document.getElementById('createbutton').className = 'btn btn-primary btn-success btn-lg btn-block';
         $('#createbutton').prop('disabled', false);
       }
     }
  };
};

// Only allow create button to be clicked once
$('input[type=submit]').one('submit', function() {
     $(this).attr('disabled','');
 });
