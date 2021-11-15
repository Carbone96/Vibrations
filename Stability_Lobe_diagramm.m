%% Theoretical Stability Lobe diagram 

% (1). Data

nat_freq = [131.02, 180.47, 188.88, 209.21, 260.38, 295.88, 315.79, 389.29,397.74, 409.95]; % frequency [Hz]
khi = [1.93, 2.15, 3.27, 2.19, 2.83, 2.34, 0.11, 2, 1.73, 1.62]/100; %damping in '%'


%% (1.a) Average number of teeth

n_teeth = 4; % number of teeth on the cutting tool
Pr = 0.005; % radial depth of cut [m]
Phi_h = 0.020; % diameter of the cutting tool [m]

m = n_teeth/2 * Pr/Phi_h; % Average number of teeth curing the cut

%% (1.b) Determination of the real and imaginary parts of the TF for each mode


len_freq_vec = 30000; % [no dim] Number of data points for around each mode (w)

total_mass = 6250; % [kg] mass = Structure + Printer head + Table

modal_Stiffness = zeros(1,10); % [N/m]
Lambda_R = zeros(10,len_freq_vec);
Lambda_I = zeros(10,len_freq_vec);
kappa = zeros(10,len_freq_vec);
%Phase = zeros(10,len_freq_vec);

% (i) Build the frequency data points around each mode (chatter frequency)

per_freq = 0.8; % Percentage of chatter frequency for half interval

data_freq_matrix = zeros(10,len_freq_vec);
for iter = 1:10
    step = (2*per_freq)*nat_freq(iter)/(len_freq_vec-1); 
    % Create an interval around each natural frequency
    %data_freq_matrix(iter,:) = (1-per_freq)*nat_freq(iter):step:(1+per_freq)*nat_freq(iter); 
    data_freq_matrix(iter,:) = (1)*nat_freq(iter):step:(1+2*per_freq)*nat_freq(iter);
 
end

% (ii) Build the Lambda_R and Lambda_I matrix for the 10 modes
for iter = 1:10
   modal_Stiffness(1,iter) = total_mass*(2*pi*nat_freq(iter))^2;
   f_n = nat_freq(iter);
   freq_vector = data_freq_matrix(iter,:);
   for j= 1:len_freq_vec
       r = freq_vector(j)/f_n;
       Lambda_R(iter,j) = (1-r^2)/(modal_Stiffness(iter)*((1-r^2)^2 + (2*khi(iter)*r)^2 )); % The '-' is just a try
       Lambda_I(iter,j) = -(2*khi(iter)*r)/(modal_Stiffness(iter)*((1-r^2)^2 + (2*khi(iter)*r)^2 ));
       kappa(iter,j) = -(2*khi(iter)*r)/(1-r^2);
   end
       
end

%% (1.c) Compute the directionnal orientation factor mu





%% (1.d) Compute the cutting stiffness Km for each chatter frequency
Kt = 5; % (seen in an another code 'processMilling.m' but should be re-measured)
Km = 5e5;
mu = 0.25;
%% (1.e) Compute the axial depth of cut around a dominant mode (w)

a_lim = zeros(10,len_freq_vec);
a_lim2 = zeros(10,len_freq_vec);
for iter=1:10
    for j=1:len_freq_vec
        % If I use 1/(...) it works more or less, but not so good either
        a_lim(iter,j) =   -2*pi * Lambda_R(iter,j) * (1+ kappa(iter,j)^2) / (n_teeth*Kt); % 
        a_lim2(iter,j) = - 1/(2*Km*mu*m*Lambda_R(iter,j)) ;
    end
end


%% (2) Compute the phase shift (epsilon) around each mode (using w) --> move around the mode with  k€N = 0,1,2,3,4,.... 

k_wave = 10; % Number of lobe considered for a dominant mode

%  Why would there be multiple lobe for one UNIQUE dominant mode ?
% --> Because depending on the RPM, the chatter can leave 1,2, ... 15 waves
% at the surface of the workpiece. This is modelled by the integer 'k_wave'
% in the formula for espilon.

epsilon = zeros(k_wave,len_freq_vec,10); 
RPM = zeros(k_wave,len_freq_vec,10);
%for c_iter = 1:10 % c_iter = chatter_iteration
   % for j=1:len_freq_vec
        % should be using cot() but whatever...
        %psi = cot(Lambda_I(c_iter,j)/Lambda_R(c_iter,j));
        %for k_iter=1:k_wave
            %epsilon(k_iter,j,c_iter) = 2*pi-2*psi + 2*(k_iter-1)*pi;
            %T = epsilon(k_iter,j,c_iter)/ (data_freq_matrix(c_iter,j)*2*pi);
            
            %epsilon(k_iter,j,c_iter) = pi + 2*psi;
           % T = (epsilon(k_iter,j,c_iter) + 2*(k_iter-1)*pi)/(2*pi*data_freq_matrix(c_iter,j));
            
            
            
          %  RPM(k_iter,j,c_iter) = 60/(n_teeth*T);
       % end
   % end        
%end

for c_iter = 1:10 % c_iter = chatter_iteration
    for j=1:len_freq_vec
        % should be using cot() but whatever...
        psi = atan2(Lambda_I(c_iter,j),Lambda_R(c_iter,j));
        for k_iter=1:k_wave
            %epsilon(k_iter,j,c_iter) = 2*pi-2*psi + 2*(k_iter-1)*pi;
            %T = epsilon(k_iter,j,c_iter)/ (data_freq_matrix(c_iter,j)*2*pi);
            
            epsilon(k_iter,j,c_iter) = pi - 2*psi;
            T = (epsilon(k_iter,j,c_iter) + 2*(k_iter-1)*pi)/(2*pi*data_freq_matrix(c_iter,j));
            
            
            
            RPM(k_iter,j,c_iter) = 60/(n_teeth*T);
        end
    end        
end




%% (3) Compute the stability diagram for each mode of the machine (Do they overlap, leading to one big graphic ??)

for c_iter=1:3
    a2plot = a_lim2(c_iter,:);
    fig = figure;
    hold on
    for k_iter=1:k_wave
        
        RPM2plot = RPM(k_iter,:,c_iter);
        plot(RPM2plot,a2plot)
        
    end
    
end







