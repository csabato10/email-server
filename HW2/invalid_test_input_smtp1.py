# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.

import sys

# Errors from Write-up
sys.stdout.write("MAILFROM: <jeffay@cs.unc.edu>\n")
sys.stdout.write("MAIL FROM <jeffay@cs.unc.edu>\n")
sys.stdout.write("RCPT TO : < bob@cs.unc.edu>\n")
sys.stdout.write("MAIL      FROM: <jeffay @cs.unc.edu>\n")

sys.stdout.write("MAIL FROM: <jeffay@cs.unc.edu>\n")
sys.stdout.write("RCPT TO: < bob@cs.unc.edu\n")
sys.stdout.write("MAILFROM: <jeffay @cs.unc.edu>\n")

# Order Error Message
sys.stdout.write("MAIL FROM: <pass@cs.unc.edu>\n")
sys.stdout.write("RCPT   TO:   <pass_again@cs.unc.edu>\n")
sys.stdout.write("MAIL FROM: <incorrect@order.com>\n")

# Command Error Message
sys.stdout.write("MAIL FROM: <pass@cs.unc.edu>\n")
sys.stdout.write("RCPT   TO:   <pass_again@cs.unc.edu>\n")
sys.stdout.write("DATA  e\n")

# Command Error Message 2
sys.stdout.write("MAIL FROM: <pass@cs.unc.edu>\n")
sys.stdout.write("RCPT   TO:   <pass_again@cs.unc.edu>\n")
sys.stdout.write("DaTA  e\n")

# Incorrect Order Message
sys.stdout.write("MAIL FROM: <pass@cs.unc.edu>\n")
sys.stdout.write("DATA\n")
sys.stdout.write("RCPT   TO:   <pass_again@cs.unc.edu>\n")

sys.stdout.write("MAIL FROM: <pass@cs.unc.edu>\n")
sys.stdout.write("XDATA\n")