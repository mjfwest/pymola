model F
  model A
    Real x;
  end A;
  A z;
end F;

model D
  replaceable model C
    replaceable model B
      Real y;
    end B;

    B z;
  end C;
  extends C;
end D;

// We can redeclare all we want, but the extends processing is handled _before_ redeclarations.
model E
  extends D(z.y(nominal=2), redeclare model C=F);
end E;
