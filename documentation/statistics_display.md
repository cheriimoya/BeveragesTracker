Statistics Display
===

The statistics display shows you, obviously, statistics about the consumption
of the items, in our case it's beverages in our students council.

It is started in its own thread, completely separate to the `BeveragesTracker`
that's why it's probably going to become a project on its own.  It will be run
with a `python3 __main__.py` in the `./beveragesplot/` directory.  This will
render the statistics as images to the current directory.  To view them, you
can use the program `feh`.

This feh command will enable a diashow, constantly refreshing the images in the
queue: `feh -A\; -Z -D5 *.png`

Here are some examples:

A pie chart diagram
![pie chart](documentation/files/pie_chart.png)

A detailed bar diagram on who takes what
![detailed chart](documentation/files/detailed_chart.png)

A diagram of the debts
![debt chart](documentation/files/debt_chart.png)

A diagram of liters drank
![liter chart](documentation/files/liter_chart.png)

One single drink in detail
![single drink](documentation/files/single_drink.png)
