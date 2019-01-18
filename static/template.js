var inputenable = true;

function select_val() 
{
	d = document.getElementById("soflow").value;
	return d;
}
  

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

(function () {
	

    var Message;

    Message = function (arg) {

        this.text = arg.text, this.message_side = arg.message_side;

        this.draw = function (_this) {
            return function () {

                var $message;

                $message = $($('.message_template').clone().html());

                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
				
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);

        return this;

    };



    $(function () {

        var getMessageText, message_side , sendMessage;

        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();			
        };

		checkMessage = function (text) {


            var $message;

            $message = $($('.message_template').clone().html());

            $message.addClass('left').find('.text').html("機器人輸入中...");
            $('.messages').append($message);
            $message.addClass('waitrobot');
            setTimeout(function () {
            $message.addClass('appeared');
            }, 0);

            

			var $messages, message, $responseContent;

			if (text.trim() === '') {
				return;
			}

			$messages = $('.messages');
			message_side = 'left';
			
			$.ajax
			(
				{
                  
					url: "/inputparser",
                    data:{'inputtext':text},
				    type:'post',
                    dataType:'json', //後端須返回json型態(需用jsonify)
					error: function(xhr) 
					{
						console.log('Ajax request error');
					},
					success: function(response) 
					{

						if (response.length>0){

                            $responseContent = response.split("@@@");
                            console.log($responseContent)


                            if($responseContent){


                                for (var i = 0; i < $responseContent.length; i++) { 

                                    message = new Message({
                                        text: $responseContent[i],
                                        message_side: message_side
                                    }); 
                                   

                                    (function(mes){
                                        {
                                            setTimeout(function(){
                                            $(".waitrobot").remove();
                                            mes.draw();
                                            $messages.animate({ scrollTop: $messages.prop('scrollHeight')} ); 
                                            },500);
         
                                        }
                                    })(message);

                                }     

                                  setTimeout(function(){
                                                inputenable =true;                                                                                           
                                            },500);             
                            } 

                        }

                        console.log(response);

					}	

				}
			);
					
        };
        
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                console.log("empty input!!!");
                inputenable = true;
                return;
            }
            $('.message_input').val(''); /* 將input的內容設為''(清空input內容) */
            $messages = $('.messages');
            message_side = 'right';
			message = new Message({
				text: text,
				message_side: message_side
			});
            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

            checkMessage(text);

        };

		firstMessage = function (text) {

            var $messages, message;

            if (text.trim() === '') {
                return;
            }

            $('.message_input').val('');

            $messages = $('.messages');
            message_side = 'left';
			message = new Message({
				text: text,
				message_side: message_side
			});


            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

        };


        $('.send_message').click(function (e) {

                if(inputenable==true){

                    inputenable = false ;
                    $temp_message = getMessageText();
                    sendMessage($temp_message);
                    // checkMessage($temp_message);

                }

                else
                {
                    return ;
                }

        });

        $('.message_input').keyup(function (e) {

            if (e.which === 13) {

                if(inputenable==true){

                    inputenable = false ;
                    $temp_message = getMessageText();
    				sendMessage($temp_message);
                    // checkMessage($temp_message);

                }

                else
                {
                    return ;
                }

            }

        });
		


		firstMessage("你好，歡迎使用本旅遊整合客服系統!");
        firstMessage("本系統目前提供 叫車 、訂車票 、訂飯店和預定(查詢)餐廳 的服務。");
        firstMessage("請問需要什麼服務呢??");


    
    });

}.call(this));