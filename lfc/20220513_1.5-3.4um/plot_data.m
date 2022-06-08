close all
clear
clc
%% plot spectrum trace under each attenuation
figure('Position', [100 100 1000 500])
hold on
load(strcat( "disp2_2.145_disp3_-0.05_ptamp_4.5A_1.5-2.7um.mat"))
plot(OSAWavelength, OSAPower, 'DisplayName','broad band LFC', 'Linewidth', 1)


ylim([-70 10])
xlabel('Wavelength(nm)')
ylabel('Power(dbm)')
legend('location','best')
set(gca,'tickdir','out');
set(gca,'box','on');
grid on
ax2 = axes('Position',get(gca,'Position'),...
           'XAxisLocation','top',...
           'YAxisLocation','right',...
           'Color','none',...
           'XColor','k','YColor','k');
set(ax2,'YTick', []);
set(ax2,'XTick', []);
title(strcat("Broader comb"))



