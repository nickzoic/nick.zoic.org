scale([0.1,0.1,0.1]) {

linear_extrude(height=10) import("python3confirmed.svg", center=true);

translate([-60,0,0]) 
difference() {
    cylinder(r=350,h=5);
    for (x = [-350:15:350]) {
        for (y=[-350:11:350]) {
            x2 = x + (y%2) * 7.5;
            translate([x2,y,-1])
            cylinder(r=5,h=10);
        }
    }
}

intersection() {
    translate([-60,0,0]) cylinder(r=280,h=20);
    linear_extrude(height=15)
    import("python3confirmed.svg", center=true);
}

/*
difference() {
    translate([310,240,0]) cylinder(r=120,h=15);
    linear_extrude(height=25)
    import("python3confirmed.svg", center=true);
}
*/
}