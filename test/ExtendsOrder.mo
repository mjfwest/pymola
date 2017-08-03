// Taken from https://trac.modelica.org/Modelica/ticket/1829#comment:38

model BT
  parameter Real m = -1;
    Real x;
  equation
    x = m;
end BT;

model M
  model A
    replaceable model AT
      Real x;
      parameter Real m = -10;
    equation
      x = m;
    end AT;
    AT at;
  end A;

  model B
    model BT
      Real x;
      parameter Real m = 0;
    equation
      x = m;
    end BT;
    BT bt;
  end B;

  extends A(redeclare model AT = BT); // Here we want to find M.BT, not .BT
  extends B;
end M;
