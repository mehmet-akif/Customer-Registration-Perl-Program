#!/usr/bin/perl

use strict;
use warnings;
use CGI;

my $cgi = CGI->new;

my $first_name    = $cgi->param('first_name');
my $last_name     = $cgi->param('last_name');
my $street_name   = $cgi->param('street_name');
my $city          = $cgi->param('city');
my $postal_code   = $cgi->param('postal_code');
my $province      = $cgi->param('province');
my $phone_number  = $cgi->param('phone_number');
my $email         = $cgi->param('email');
my $photo         = $cgi->param('photo');

my $error_message = '';

if ($first_name eq '' || $first_name !~ /^[a-zA-Z]+$/) {
    $error_message .= "(Invalid First Name.) ";
}
if ($last_name eq '' || $last_name !~ /^[a-zA-Z]+$/) {
    $error_message .= "(Invalid Last Name.) ";
}
if ($street_name eq '') {
    $error_message .= "(Please enter a city name.) ";
}
if ($city eq '') {
    $error_message .= "(Please enter a city name.) ";
}
if ($postal_code eq '' || $postal_code !~ /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/) {
    $error_message .= "(Invalid Postal Code.) ";
}
if ($province eq '') {
    $error_message .= "(please choose one of the provinces.) ";
}
if ($phone_number eq '' || $phone_number !~ /^\d{10}$/) {
    $error_message .= "(Invalid Phone Number.) ";
}
if ($email eq '' || $email !~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) {
    $error_message .= "(Invalid Email Address.) ";
}
my ($photo_extension) = $photo =~ /\.([^.]+)$/;
my @allowed_extensions = qw(png gif jpg jpeg);

if (!defined $photo_extension || !grep { lc($photo_extension) eq $_ } @allowed_extensions) {
    $error_message .= "(Invalid Photo Format. Upload a .png, .gif, or .jpeg file.) ";
}
if ($error_message) {
    print $cgi->header;
    print $cgi->start_html("Error");
    print "<style>body{font-family: Arial, sans-serif;background-color: #f4f4f4;margin: 0;padding: 0;}.container{width: 50%;margin: auto;overflow: hidden;}.error{color: red;}.display-info{max-width: 600px;margin: 20px auto;padding: 20px;background: #fff;border-radius: 5px;box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);}.display-info h2{color: #333;}.info{margin-bottom: 10px;}.photo img{max-width: 100%;border-radius: 5px;}</style>";
    print $cgi->start_body;
    print "<div class='container'>";
    print "<div class='display-info'>";
    print "<h2><b> Somethings seems missing or invalid. Please Try Again </b></h2>";
    print "<p class='error'><b>$error_message</b></p>";


    print "<ul>";
    print "<li class='error'>First Name</li>" if ($first_name eq '' || $first_name !~ /^[a-zA-Z]+$/);
    print "<li class='error'>Last Name</li>" if ($last_name eq '' || $last_name !~ /^[a-zA-Z]+$/);
    print "<li class='error'>Street Name</li>" if ($street_name eq '');
    print "<li class='error'>City</li>" if ($city eq '');
    print "<li class='error'>Postal Code</li>" if ($postal_code eq '' || $postal_code !~ /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/);
    print "<li class='error'>Province</li>" if ($province eq '');
    print "<li class='error'>Phone Number</li>" if ($phone_number eq '' || $phone_number !~ /^\d{10}$/);
    print "<li class='error'>Email</li>" if ($email eq '' || $email !~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/);
    print "<li class='error'>Photograph</li>" if (!defined $photo_extension || !grep { lc($photo_extension) eq $_ } @allowed_extensions);
    print "</ul>";

    print "</div>";
    print "</div>";
    print $cgi->end_html;
} else {

    my $upload_dir  = "uploads";
    my $upload_file = "$upload_dir/$first_name$last_name.$photo_extension";
    open my $photo_fh, '>', $upload_file or die "Cannot open file: $!";
    while (my $bytes = $photo->read(my $buffer, 4096)) {
        print $photo_fh $buffer;
    }
    close $photo_fh;


    print $cgi->header;
    print $cgi->start_html("Submission Successful");
    print "<style>body{font-family: Arial, sans-serif;background-color: #f4f4f4;margin: 0;padding: 0;}.container{width: 50%;margin: auto;overflow: hidden;}.display-info{max-width: 600px;margin: 20px auto;padding: 20px;background: #fff;border-radius: 5px;box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);}.display-info h2{color: #333;}.info{margin-bottom: 10px;}.photo img{max-width: 100%;border-radius: 5px;}</style>";
    print $cgi->start_body;
    print "<div class='container'>";
    print "<div class='display-info'>";
    print "<h2> INFORMATIONS PROVIDED: </h2>";
    print "<div class='info'><strong>First Name:</strong> $first_name</div>";
    print "<div class='info'><strong>Last Name:</strong> $last_name</div>";
    print "<div class='info'><strong>Street Name:</strong> $street_name</div>";
    print "<div class='info'><strong>City:</strong> $city</div>";
    print "<div class='info'><strong>Postal Code:</strong> $postal_code</div>";
    print "<div class='info'><strong>Province:</strong> $province</div>";
    print "<div class='info'><strong>Phone Number:</strong> $phone_number</div>";
    print "<div class='info'><strong>Email:</strong> $email</div>";
    print "<div class='info'><strong>Photograph:</strong><br><div class='photo'><img src='$upload_file' alt='Uploaded Photograph'></div></div>";
    print "</div>";
    print "</div>";
    print $cgi->end_html;
}