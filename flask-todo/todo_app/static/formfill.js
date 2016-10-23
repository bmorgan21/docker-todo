$.fn.values = function(data) {
   var inps = $(this).find(":input").get();

    if(typeof data != "object") {
       // return all data
        data = {};

        $.each(inps, function() {
            if (this.name && (this.checked
                        || /select|textarea/i.test(this.nodeName)
                        || /text|hidden|password/i.test(this.type))) {
                data[this.name] = $(this).val();
            }
        });
        return data;
    } else {
        $.each(inps, function() {
            if (this.name && this.name in data) {
                if ($(this).hasClass('default-value')) {
                    // do nothing, these should remain what they are.
                    // this is used for setting the non-checked value of a checkbox
                } else if(this.type == "checkbox" || this.type == "radio") {
                    var checked;
                    if (typeof data[this.name] == 'object') {
                        checked = _.map(data[this.name], function(el, i) {return "" + el;}).indexOf($(this).val()) != -1;
                    } else {
                        checked = ''+data[this.name] == $(this).val();
                    }
                    $(this).prop("checked", checked);
                } else if ('object' != typeof data[this.name] || data[this.name] == null) {
                    $(this).val(data[this.name]);
                } else {
                    $(this).val(JSON.stringify(data[this.name]));
                }
                $(this).removeClass('mui--is-empty').addClass('mui--is-not-empty');
            } else if (this.type == "checkbox") {
                $(this).prop("checked", false);
                $(this).removeClass('mui--is-empty').addClass('mui--is-not-empty');
            }
       });
       return $(this);
    }
};

$.fn.errors = function(data) {
   var inps = $(this).find(":input").get();

    if(data && typeof data == "object") {
        $.each(inps, function() {
            if (this.name && data[this.name]) {
                var $form_group = $(this).closest('.form-group');
                var $input_group = $(this).closest('.input-group');
                var $form_control_inline = $(this).closest('.form-control-inline');

                var $element = $(this);
                var is_multi = $form_group.hasClass('multi');
                if ($input_group.length != 0) {
                    $element = $input_group;
                } else if ($form_control_inline.length != 0) {
                    $element = $form_control_inline;
                }

                var $block = $element.next('.help-block');
                if (!is_multi && $block.length == 0) {
                    $block = $form_group.find('.help-block');
                }

                if ($block.length == 0) {
                    $block = $(this).closest('form').find('.help-block.default');
                }

                if ($block.length == 0) {
                    $block = $('<span class="help-block" style="display:none;"></span>');
                    $element.after($block);
                }

                var $error_block = $form_group;
                if (is_multi) {
                    $error_block = $element;
                }

                if (!$error_block) {
                    $error_block = $block.parent();
                }
                $error_block.addClass('has-error');
                $block.html("<span class='fa fa-exclamation-circle'></span> " + data[this.name]).show();
            }
       });
       return $(this);
    }
};
