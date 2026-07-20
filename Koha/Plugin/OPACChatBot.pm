package Koha::Plugin::OPACChatBot;

use Modern::Perl;
use base qw(Koha::Plugins::Base);

our $metadata = {
    name            => 'OPAC AI Assistant',
    author          => 'Hasnat Khan',
    description     => 'Simple chatbot for Koha OPAC',
    date_authored   => '2026-07-05',
    date_updated    => '2026-07-05',
    minimum_version => '26.05',
    maximum_version => undef,
    version         => '1.0.1',
};

sub new {
    my ( $class, $args ) = @_;
    $args->{metadata} = $metadata;
    return $class->SUPER::new($args);
}

sub opac_head {
    my ( $self ) = @_;
    my $css_dir = $self->get_plugin_dir() . '/css';
    my $css = '';
    
    if ( -d $css_dir ) {
        opendir(my $dh, $css_dir);
        my @files = sort grep { /\.css$/ && -f "$css_dir/$_" } readdir($dh);
        closedir($dh);
        
        foreach my $file (@files) {
            if (open my $fh, '<', "$css_dir/$file") {
                local $/;
                $css .= <$fh> . "\n";
                close $fh;
            }
        }
    }
    
    return "<style>\n$css\n</style>" if $css;
    return '';
}

sub opac_js {
    my ( $self ) = @_;
    my $js_dir = $self->get_plugin_dir() . '/js';
    my $js = '';
    
    # Define correct load order for frontend JavaScript
    my @files = qw(
        config.js
        icons.js
        utils.js
        faq.js
        knowledgeBase.js
        intentEngine.js
        api.js
        ui.js
        chatController.js
        app.js
    );
    
    foreach my $file (@files) {
        if ( -f "$js_dir/$file" && open my $fh, '<', "$js_dir/$file" ) {
            local $/;
            $js .= "/* --- $file --- */\n" . <$fh> . "\n\n";
            close $fh;
        }
    }
    
    return "<script>\n$js\n</script>" if $js;
    return '';
}

1;
