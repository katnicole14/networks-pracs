#!/usr/bin/perl

use strict;
use warnings;

# Function to calculate the next Fibonacci number
sub next_fibonacci {
    my ($fib_file) = @_;

    # Open the file
    open my $fh, '<', $fib_file or die "Error: Unable to open file $fib_file: $!";
    my $line = <$fh>;
    close $fh;

    # Read the Fibonacci numbers from the file
    my @fib_numbers = split ' ', $line;

    # Calculate the next Fibonacci number by extracting the last two numbers
    my ($num1, $num2) = @fib_numbers[-2, -1];
    my $next_fib = $num1 + $num2;

    return $next_fib;
}

# Function to update the Fibonacci sequence in the file
sub update_file {
    my ($fib_file, $fib_numbers, $next_fib) = @_;

    # Remove the first number
    shift @$fib_numbers;

    # Add the next Fibonacci number
   push @$fib_numbers, $next_fib;

      # Write the updated sequence back to the file
    open my $fh, '>', $fib_file or die "Error: Unable to open file $fib_file: $!";

   print $fh join(' ', @$fib_numbers);
   close $fh;
}


# Function to generate HTML output
sub generate_html {
    my ($next_fib, $fib_file, @fib_numbers) = @_;

    # Generate HTML content
    print "Content-type: text/html\n\n";
    print "<!DOCTYPE html>\n";
    print "<html>\n";
    print "<head>\n";
    print "<title>Next Fibonacci Number</title>\n";
    print "</head>\n";
    print "<body>\n";
    print "<h1>Fibonacci Numbers:</h1>\n";

    foreach my $num (@fib_numbers) {
        print "<p>$num</p>\n";
    }
 print "<h1>Next Fibonacci Number</h1>";
    print "<p>$next_fib</p>\n";
    print "</body>\n";
    print "</html>\n";
}

# main code
my $fib_file = "/usr/lib/cgi-bin/fibonacci.txt";
# Call the next_fibonacci function to calculate the next Fibonacci number
my $next_fib = next_fibonacci($fib_file);

# Read the updated sequence from the file
open my $fh, '<', $fib_file or die "Error: Unable to open file $fib_file: $!";
my $line = <$fh>;
close $fh;
my @fib_numbers = split ' ', $line;


# Call the generate_html function to display the result
generate_html($next_fib, $fib_file, @fib_numbers);

# Call the update_file function to update the sequence in the file
update_file($fib_file, \@fib_numbers, $next_fib);

#print  the new sequence
print "<p>NEW FIBOBACCI NUMBERS</p>";
 foreach my $num (@fib_numbers) {
        print "<p>$num</p>\n";
    }
#print the  links 
print "<a href=\"/cgi-bin/next.cgi\">Next</a>\n";
    print "<a href=\"/cgi-bin/previous.cgi\">Previous</a>\n";
