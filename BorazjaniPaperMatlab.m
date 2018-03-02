% Mendelson Lab - another shot at the Borazjani paper

% Present in the Mathematica File, not sure why
rho = 1;
s = 1;
l = 1;

% Wave Parameters
% Note: I'm not really sure where half these constants come from
dimLam = 0.95;
L = 1;
k = 2*pi/(dimLam*1);
omega = 2*pi*0.3/(2*.01);

% Constants for the function a
a0 = 0.02;
a1 = -0.08;
a2 = 0.16;
amax = L*0.1;

times = [0, 0.1, 0.2, 0.3, 0.5, 1, 2, 4, 9, 10, 20];

% It still doesn't work...
aFxn = @(z) a0 + a1.*z +a2.*(z.^2);
hFxn1 = @(z) aFxn(z).*sin(k.*z-omega.*times(1));
hFxn2 = @(z) aFxn(z).*sin(k.*z-omega.*times(2));
hFxn3 = @(z) aFxn(z).*sin(k.*z-omega.*times(3));
hFxn4 = @(z) aFxn(z).*sin(k.*z-omega.*times(4));
hFxn5 = @(z) aFxn(z).*sin(k.*z-omega.*times(5));
hFxn6 = @(z) aFxn(z).*sin(k.*z-omega.*times(6));

z = [0:0.01:1];
hVals1 = hFxn1(z);
hVals2 = hFxn2(z);
hVals3 = hFxn3(z);
hVals4 = hFxn4(z);
hVals5 = hFxn5(z);
hVals6 = hFxn6(z);

plot(z, hVals1, hVals2, hVals3);