#!/usr/bin/perl

use strict;
use warnings;

# Function to read the Fibonacci numbers from the file
sub read_fibonacci {
    my ($fib_file) = @_;
    open my $fh, '<', $fib_file or die "Error: Unable to open file $fib_file: $!";
    my $line = <$fh>;
    close $fh;
    return split ' ', $line;
}

# Function to write the Fibonacci numbers to the file
sub write_fibonacci {
    my ($fib_file, @fib_numbers) = @_;
    open my $fh, '>', $fib_file or die "Error: Unable to open file $fib_file: $!";
    print $fh join(' ', @fib_numbers);
    close $fh;
}

# Function to calculate the next Fibonacci number
sub next_fibonacci {
    my ($x, $y, $z) = @_;
    return ($y - $x, $x, $y);
}

# Main code
my $fib_file = "/usr/lib/cgi-bin/fibonacci.txt";

# Read Fibonacci numbers from the file
my @fib_numbers = read_fibonacci($fib_file);

# Calculate the next Fibonacci number
my ($next_x, $next_y, $next_z) = next_fibonacci(@fib_numbers);

# Write the updated sequence back to the file
write_fibonacci($fib_file, $next_x, $next_y, $next_z);

# Generate HTML output
print "Content-type: text/html\n\n";
print "<!DOCTYPE html>\n";
print "<html>\n";
print "<head>\n";
print "</head>\n";
print "<body>\n";
print "<h1> Numbers:</h1>\n";
print "<p>($next_x, $next_y, $next_z)</p>\n";

#print the next link
print "<a href=\"/cgi-bin/next.cgi\">Next</a>\n";

#user base case for the (0,1,1) case 

    # Check if the current sequence is (0, 1, 1) to disable "Previous" link
    if ($fib_numbers[0] == 0 && $fib_numbers[1] == 1 && $fib_numbers[2] == 1) {
        print "<a>Previous</a>\n";  # Print "Previous" link without a hyperlink
    } else {
        print "<a href=\"previous.cgi\">Previous</a>\n";  # Print "Previous" link with correct hyperlink
    }

print "</body>\n";
print "</html>\n";

