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

1;
